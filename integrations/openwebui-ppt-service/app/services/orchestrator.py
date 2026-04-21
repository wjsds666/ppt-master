from __future__ import annotations

import json
import os
import shutil
import sys
from pathlib import Path
from textwrap import dedent
from typing import Any

from app.core.command_runner import run_command
from app.core.job_store import JobStore
from app.core.runtime_config import RuntimeConfigStore
from app.core.settings import Settings
from app.schemas.jobs import (
    JobInput,
    PlanResult,
    SlidePlan,
    ensure_svg_file_name,
)
from app.services.llm_client import LLMClient, extract_code_block


STYLE_FILE_MAP = {
    "general_versatile": "executor-general.md",
    "general_consulting": "executor-consultant.md",
    "top_consulting": "executor-consultant-top.md",
}


class PPTOrchestrator:
    def __init__(self, settings: Settings, job_store: JobStore) -> None:
        self.settings = settings
        self.job_store = job_store
        self.runtime_config = RuntimeConfigStore(settings)
        self.llm = LLMClient(settings, self.runtime_config)
        self.skill_dir = settings.repo_root / "skills" / "ppt-master"
        self.references_dir = self.skill_dir / "references"
        self.templates_dir = self.skill_dir / "templates"
        self.tools_python = os.getenv("PPT_MASTER_PYTHON", sys.executable)

    def run_job(self, job: dict[str, Any]) -> dict[str, Any]:
        job_id = job["job_id"]
        payload = JobInput(**job["payload"])
        self._apply_image_toggle(job_id, payload)
        project_path = self._prepare_project(job_id, payload)
        source_markdown = self._load_source_markdown(project_path)
        plan = self._create_plan(job_id, payload, source_markdown)
        self._write_design_spec(project_path, payload, plan)
        self._copy_template_assets(project_path, payload)
        self._generate_svg_pages(job_id, project_path, payload, plan)
        self._generate_notes(job_id, project_path, payload, plan)
        artifacts = self._finalize_exports(job_id, project_path)
        return artifacts

    def _apply_image_toggle(self, job_id: str, payload: JobInput) -> None:
        runtime = self.runtime_config.load()
        ai_image_enabled = bool(runtime.get("ai_image_enabled", False))
        requested = (payload.image_strategy or "").strip().lower()
        wants_ai = requested in {"ai_generation", "ai_generate", "ai", "generate"}
        if not ai_image_enabled and wants_ai:
            payload.image_strategy = "placeholder"
            self.job_store.append_log(
                job_id,
                "AI image is disabled in /admin. Falling back to placeholder image strategy.",
            )
            return
        if ai_image_enabled and wants_ai and not str(runtime.get("image_api_key") or "").strip():
            raise RuntimeError(
                "AI image is enabled but image_api_key is empty. "
                "Please fill it in /admin before enabling AI image generation."
            )

    def _prepare_project(self, job_id: str, payload: JobInput) -> Path:
        job_paths = self.job_store.get_paths(job_id)
        projects_base = job_paths.project_root
        projects_base.mkdir(parents=True, exist_ok=True)

        init_output = run_command(
            [
                self.tools_python,
                str(self.skill_dir / "scripts" / "project_manager.py"),
                "init",
                payload.project_name,
                "--format",
                payload.canvas_format,
                "--dir",
                str(projects_base),
            ],
            cwd=self.settings.repo_root,
            job_store=self.job_store,
            job_id=job_id,
        )
        project_path = self._extract_project_path(init_output)
        self.job_store.append_log(job_id, f"Project workspace: {project_path}")

        if payload.uploaded_file_path:
            run_command(
                [
                    self.tools_python,
                    str(self.skill_dir / "scripts" / "project_manager.py"),
                    "import-sources",
                    str(project_path),
                    payload.uploaded_file_path,
                    "--move",
                ],
                cwd=self.settings.repo_root,
                job_store=self.job_store,
                job_id=job_id,
            )
        elif payload.source_url:
            run_command(
                [
                    self.tools_python,
                    str(self.skill_dir / "scripts" / "project_manager.py"),
                    "import-sources",
                    str(project_path),
                    payload.source_url,
                    "--move",
                ],
                cwd=self.settings.repo_root,
                job_store=self.job_store,
                job_id=job_id,
            )
        elif payload.source_text:
            source_path = project_path / "sources" / "source_text.md"
            source_path.write_text(payload.source_text, encoding="utf-8")
            self.job_store.append_log(job_id, f"Wrote inline source to {source_path}")
        else:
            raise RuntimeError("No source content was provided.")

        return project_path

    def _load_source_markdown(self, project_path: Path) -> str:
        candidates = sorted(project_path.glob("sources/**/*.md"))
        if not candidates:
            candidates = sorted(project_path.glob("sources/**/*.txt"))
        parts: list[str] = []
        for path in candidates:
            if path.name == "README.md":
                continue
            parts.append(f"\n# Source: {path.name}\n\n{path.read_text(encoding='utf-8', errors='replace')}")
        if not parts:
            raise RuntimeError("No normalized markdown source was found in sources/.")
        return "\n".join(parts)[:50000]

    def _create_plan(self, job_id: str, payload: JobInput, source_markdown: str) -> PlanResult:
        strategist = (self.references_dir / "strategist.md").read_text(encoding="utf-8")
        design_spec_reference = (self.templates_dir / "design_spec_reference.md").read_text(encoding="utf-8")
        system_prompt = dedent(
            """
            You are the Strategist for PPT Master.
            Produce a single JSON object only.
            Follow the repository constraints:
            - Respect the eight confirmations from strategist.md, but auto-decide based on user input.
            - Create a concise but executable slide plan.
            - Keep page count close to the requested value.
            - Use safe, realistic icon names from tabler-outline or tabler-filled only.
            - Avoid fabricated precise statistics not present in the source.
            - Use consultant style titles that are conclusion-driven when possible.
            """
        ).strip()
        user_prompt = dedent(
            f"""
            Repository guidance:
            <strategist>
            {strategist[:16000]}
            </strategist>

            Design spec reference:
            <design_spec_reference>
            {design_spec_reference[:8000]}
            </design_spec_reference>

            User request:
            - project_name: {payload.project_name}
            - canvas_format: {payload.canvas_format}
            - page_count: {payload.page_count}
            - target_audience: {payload.target_audience or "auto"}
            - use_case: {payload.use_case or "auto"}
            - style_objective: {payload.style_objective}
            - color_hint: {payload.color_hint or "auto"}
            - image_strategy: {payload.image_strategy}
            - icon_style: {payload.icon_style}
            - template_name: {payload.template_name or "none"}
            - notes_style: {payload.notes_style}
            - preferred_language: {payload.language or "auto"}

            Source markdown:
            <source_markdown>
            {source_markdown}
            </source_markdown>

            Return JSON with this shape:
            {{
              "project_summary": "...",
              "language": "zh-CN",
              "canvas_format": "{payload.canvas_format}",
              "page_count": {payload.page_count},
              "target_audience": "...",
              "use_case": "...",
              "style_objective": "{payload.style_objective}",
              "theme_mode": "light",
              "tone": "...",
              "color_scheme": {{
                "background": "#FFFFFF",
                "secondary_bg": "#F8FAFC",
                "primary": "#0F62FE",
                "accent": "#16A34A",
                "secondary_accent": "#38BDF8",
                "body_text": "#0F172A",
                "secondary_text": "#475569",
                "tertiary_text": "#94A3B8",
                "border": "#CBD5E1",
                "success": "#16A34A",
                "warning": "#DC2626"
              }},
              "typography": {{
                "preset": "P1",
                "title_font": "Microsoft YaHei",
                "body_font": "Microsoft YaHei",
                "emphasis_font": "SimHei",
                "english_title_font": "Arial",
                "english_body_font": "Calibri",
                "body_size": "18",
                "content_title_size": "30"
              }},
              "spacing": {{
                "margins": "left/right 60px, top 50px, bottom 40px",
                "card_gap": "24",
                "card_padding": "24",
                "border_radius": "16"
              }},
              "icon_usage": {{
                "mode": "built-in",
                "library": "{payload.icon_style}",
                "notes": "..."
              }},
              "image_usage": {{
                "mode": "{payload.image_strategy}",
                "notes": "..."
              }},
              "chart_refs": [
                {{"chart_type": "bar_chart", "used_in": "03_xxx", "reason": "..."}}
              ],
              "notes_plan": {{
                "total_duration": "12 minutes",
                "notes_style": "{payload.notes_style}",
                "purpose": "inform"
              }},
              "slides": [
                {{
                  "index": 1,
                  "title": "Cover Title",
                  "page_role": "cover",
                  "file_name": "01_cover.svg",
                  "layout": "full-screen cover",
                  "takeaway": "Core message",
                  "bullets": ["...", "..."],
                  "chart": "",
                  "source_note": "",
                  "image_needs": [],
                  "template_mapping": "free design"
                }}
              ]
            }}

            Rules:
            - page_role should be one of: cover, agenda, chapter, content, ending.
            - slides length must equal page_count.
            - file_name must be unique and end with .svg.
            - use source-grounded wording and avoid hallucinated references.
            """
        ).strip()
        result = self.llm.complete_json(system_prompt, user_prompt)
        slides = [
            SlidePlan(
                index=int(item["index"]),
                title=item["title"],
                page_role=item["page_role"],
                file_name=item.get("file_name") or ensure_svg_file_name(int(item["index"]), item["title"]),
                layout=item["layout"],
                takeaway=item.get("takeaway", ""),
                bullets=list(item.get("bullets", [])),
                chart=item.get("chart", ""),
                source_note=item.get("source_note", ""),
                image_needs=list(item.get("image_needs", [])),
                template_mapping=item.get("template_mapping", "free design"),
            )
            for item in result["slides"]
        ]
        if len(slides) != int(result["page_count"]):
            raise RuntimeError("Planner returned slide count inconsistent with page_count.")
        return PlanResult(
            project_summary=result["project_summary"],
            language=result["language"],
            canvas_format=result["canvas_format"],
            page_count=int(result["page_count"]),
            target_audience=result["target_audience"],
            use_case=result["use_case"],
            style_objective=result["style_objective"],
            theme_mode=result["theme_mode"],
            tone=result["tone"],
            color_scheme=result["color_scheme"],
            typography=result["typography"],
            spacing=result["spacing"],
            icon_usage=result["icon_usage"],
            image_usage=result["image_usage"],
            chart_refs=list(result.get("chart_refs", [])),
            notes_plan=result["notes_plan"],
            slides=slides,
        )

    def _write_design_spec(self, project_path: Path, payload: JobInput, plan: PlanResult) -> None:
        chart_rows = "\n".join(
            f"| {row.get('chart_type', '')} | {row.get('chart_type', '')}.svg | {row.get('used_in', '')} |"
            for row in plan.chart_refs
        ) or "| None | - | - |"
        slide_sections = []
        for slide in plan.slides:
            bullets = "\n".join(f"  - {item}" for item in slide.bullets) or "  - TBD"
            chart_line = f"- **Chart**: {slide.chart}\n" if slide.chart else ""
            slide_sections.append(
                dedent(
                    f"""
                    #### Slide {slide.index:02d} - {slide.title}

                    - **Layout**: {slide.layout}
                    - **Template mapping**: {slide.template_mapping}
                    - **Takeaway**: {slide.takeaway}
                    {chart_line}- **Content**:
                    {bullets}
                    """
                ).strip()
            )
        slide_outline = "\n\n".join(slide_sections)

        design_spec = dedent(
            f"""
            # {payload.project_name} - Design Spec

            ## I. Project Information

            | Item | Value |
            | ---- | ----- |
            | **Project Name** | {payload.project_name} |
            | **Canvas Format** | {plan.canvas_format} |
            | **Page Count** | {plan.page_count} |
            | **Design Style** | {plan.style_objective} |
            | **Target Audience** | {plan.target_audience} |
            | **Use Case** | {plan.use_case} |

            ---

            ## II. Canvas Specification

            | Property | Value |
            | -------- | ----- |
            | **Format** | {plan.canvas_format} |
            | **Margins** | {plan.spacing.get("margins", "")} |

            ---

            ## III. Visual Theme

            - **Theme**: {plan.theme_mode}
            - **Tone**: {plan.tone}
            - **Summary**: {plan.project_summary}

            | Role | HEX | Purpose |
            | ---- | --- | ------- |
            | **Background** | `{plan.color_scheme.get("background", "")}` | Page background |
            | **Secondary bg** | `{plan.color_scheme.get("secondary_bg", "")}` | Card background |
            | **Primary** | `{plan.color_scheme.get("primary", "")}` | Main emphasis |
            | **Accent** | `{plan.color_scheme.get("accent", "")}` | Highlight |
            | **Secondary accent** | `{plan.color_scheme.get("secondary_accent", "")}` | Gradient / secondary highlight |
            | **Body text** | `{plan.color_scheme.get("body_text", "")}` | Main body text |
            | **Secondary text** | `{plan.color_scheme.get("secondary_text", "")}` | Notes |
            | **Tertiary text** | `{plan.color_scheme.get("tertiary_text", "")}` | Meta text |
            | **Border/divider** | `{plan.color_scheme.get("border", "")}` | Borders |
            | **Success** | `{plan.color_scheme.get("success", "")}` | Positive |
            | **Warning** | `{plan.color_scheme.get("warning", "")}` | Risk |

            ---

            ## IV. Typography System

            - **Preset**: {plan.typography.get("preset", "")}
            - **Title font**: {plan.typography.get("title_font", "")}
            - **Body font**: {plan.typography.get("body_font", "")}
            - **Emphasis font**: {plan.typography.get("emphasis_font", "")}
            - **Body size**: {plan.typography.get("body_size", "")}px
            - **Content title size**: {plan.typography.get("content_title_size", "")}px

            ---

            ## V. Layout Principles

            - **Card gap**: {plan.spacing.get("card_gap", "")}px
            - **Card padding**: {plan.spacing.get("card_padding", "")}px
            - **Border radius**: {plan.spacing.get("border_radius", "")}px

            ---

            ## VI. Icon Usage Specification

            - **Mode**: {plan.icon_usage.get("mode", "")}
            - **Library**: {plan.icon_usage.get("library", "")}
            - **Notes**: {plan.icon_usage.get("notes", "")}

            ---

            ## VII. Chart Reference List

            | Chart Type | Reference Template | Used In |
            | ---------- | ------------------ | ------- |
            {chart_rows}

            ---

            ## VIII. Image Resource List

            | Filename | Dimensions | Ratio | Purpose | Type | Status | Generation Description |
            | -------- | ---------- | ----- | ------- | ---- | ------ | --------------------- |
            | auto | auto | auto | {plan.image_usage.get("notes", "")} | Mixed | {plan.image_usage.get("mode", "")} | {plan.image_usage.get("notes", "")} |

            ---

            ## IX. Content Outline

            {slide_outline}

            ---

            ## X. Speaker Notes Plan

            - **Total duration**: {plan.notes_plan.get("total_duration", "")}
            - **Style**: {plan.notes_plan.get("notes_style", "")}
            - **Purpose**: {plan.notes_plan.get("purpose", "")}
            """
        ).strip() + "\n"
        (project_path / "design_spec.md").write_text(design_spec, encoding="utf-8")

    def _copy_template_assets(self, project_path: Path, payload: JobInput) -> None:
        if not payload.template_name:
            return
        source_dir = self.templates_dir / "layouts" / payload.template_name
        if not source_dir.exists():
            raise RuntimeError(f"Template not found: {payload.template_name}")
        target_dir = project_path / "templates"
        for path in source_dir.iterdir():
            if path.is_file():
                shutil.copy2(path, target_dir / path.name)

    def _generate_svg_pages(
        self,
        job_id: str,
        project_path: Path,
        payload: JobInput,
        plan: PlanResult,
    ) -> None:
        executor_base = (self.references_dir / "executor-base.md").read_text(encoding="utf-8")
        shared = (self.references_dir / "shared-standards.md").read_text(encoding="utf-8")
        style_reference = self._load_style_reference(plan.style_objective)
        for slide in plan.slides:
            template_content = self._load_template_reference(project_path, slide.page_role)
            self.job_store.append_log(job_id, f"Generating slide {slide.index:02d}: {slide.title}")
            base_prompt = dedent(
                f"""
                Common executor rules:
                <executor_base>
                {executor_base[:10000]}
                </executor_base>

                Shared technical standards:
                <shared_standards>
                {shared[:10000]}
                </shared_standards>

                Style reference:
                <style_reference>
                {style_reference[:7000]}
                </style_reference>

                Design spec:
                <design_spec>
                {(project_path / "design_spec.md").read_text(encoding="utf-8")[:16000]}
                </design_spec>

                Template reference:
                <template_reference>
                {template_content}
                </template_reference>

                Generate exactly one SVG page.
                Requirements:
                - Output raw SVG only, no prose.
                - File name: {slide.file_name}
                - Page role: {slide.page_role}
                - Page title: {slide.title}
                - Layout: {slide.layout}
                - Takeaway: {slide.takeaway}
                - Bullet points: {json.dumps(slide.bullets, ensure_ascii=False)}
                - Chart: {slide.chart or "none"}
                - Source note: {slide.source_note or "none"}
                - Image needs: {json.dumps(slide.image_needs, ensure_ascii=False)}
                - Use {plan.icon_usage.get("library", payload.icon_style)} icons only when necessary.
                - Keep the SVG PowerPoint-safe: no clipPath, no mask, no style tag, no class, no foreignObject.
                - Add logical <g> groups for editable PowerPoint groups.
                - Include a background rect.
                """
            ).strip()
            svg_text = self._generate_single_svg_with_retry(base_prompt)
            (project_path / "svg_output" / slide.file_name).write_text(svg_text + "\n", encoding="utf-8")

    def _generate_single_svg_with_retry(self, base_prompt: str) -> str:
        last_error: Exception | None = None
        for attempt in range(3):
            prompt = base_prompt
            if attempt > 0:
                prompt = (
                    f"{base_prompt}\n\n"
                    "IMPORTANT RETRY INSTRUCTION:\n"
                    "Return a complete <svg>...</svg> document only.\n"
                    "No markdown fences.\n"
                    "No explanation text.\n"
                    "The first non-space character must be '<'."
                )
            try:
                svg = self.llm.complete_text(
                    "You are the PPT Master Executor. Return one valid SVG document only.",
                    prompt,
                    temperature=0.15,
                )
                svg_text = extract_code_block(svg, "svg")
                self._validate_svg(svg_text)
                return svg_text
            except Exception as exc:  # noqa: BLE001
                last_error = exc
                continue
        if last_error is not None:
            raise last_error
        raise RuntimeError("Failed to generate SVG page.")

    def _generate_notes(
        self,
        job_id: str,
        project_path: Path,
        payload: JobInput,
        plan: PlanResult,
    ) -> None:
        slides_json = [
            {
                "index": slide.index,
                "title": slide.title,
                "takeaway": slide.takeaway,
                "bullets": slide.bullets,
            }
            for slide in plan.slides
        ]
        prompt = dedent(
            f"""
            Create speaker notes for this PPT Master project.
            Language: {plan.language}
            Notes style: {plan.notes_plan.get("notes_style", payload.notes_style)}
            Purpose: {plan.notes_plan.get("purpose", "inform")}
            Total duration: {plan.notes_plan.get("total_duration", "10 minutes")}

            Slides:
            {json.dumps(slides_json, ensure_ascii=False, indent=2)}

            Output markdown only.
            Format:
            - Each page starts with "# <svg-file-name without .svg>"
            - Separate pages with "---"
            - Each page should have 2-5 natural sentences
            - Include localized "Key points:" and "Duration:" labels matching the slide language
            - From the second page onward, start with a localized transition marker
            """
        ).strip()
        notes = self.llm.complete_text(
            "You write concise, presentation-ready speaker notes in markdown only.",
            prompt,
            temperature=0.3,
        )
        normalized = notes.strip()
        if not any(line.startswith("# ") for line in normalized.splitlines()):
            normalized = self._build_fallback_notes(plan)
            self.job_store.append_log(
                job_id,
                "Notes fallback applied because model output missed '# ' headings required by total_md_split.py.",
            )
        (project_path / "notes" / "total.md").write_text(normalized + "\n", encoding="utf-8")
        self.job_store.append_log(job_id, "Speaker notes written to notes/total.md")

    @staticmethod
    def _build_fallback_notes(plan: PlanResult) -> str:
        sections: list[str] = []
        for slide in plan.slides:
            stem = Path(slide.file_name).stem
            bullets = slide.bullets[:3] if slide.bullets else [slide.takeaway or slide.title]
            bullet_line = "；".join(item for item in bullets if item) or slide.title
            sections.append(
                "\n".join(
                    [
                        f"# {stem}",
                        f"[过渡] 这一页聚焦：{slide.title}。",
                        f"重点说明：{bullet_line}。",
                        f"要点：① {slide.takeaway or slide.title} ② 信息支撑 ③ 下一步行动",
                        "时长：1 分钟",
                    ]
                )
            )
        return "\n\n---\n\n".join(sections)

    def _finalize_exports(self, job_id: str, project_path: Path) -> dict[str, Any]:
        for script_name in ("total_md_split.py", "finalize_svg.py"):
            run_command(
                [self.tools_python, str(self.skill_dir / "scripts" / script_name), str(project_path)],
                cwd=self.settings.repo_root,
                job_store=self.job_store,
                job_id=job_id,
            )
        run_command(
            [
                self.tools_python,
                str(self.skill_dir / "scripts" / "svg_to_pptx.py"),
                str(project_path),
                "-s",
                "final",
            ],
            cwd=self.settings.repo_root,
            job_store=self.job_store,
            job_id=job_id,
        )

        native_pptx = sorted(project_path.glob("*.pptx"))
        if not native_pptx:
            raise RuntimeError("No PPTX artifacts were generated.")

        artifacts: dict[str, Any] = {
            "project_path": str(project_path),
            "files": [],
        }
        for path in native_pptx:
            exported = self.job_store.export_file(job_id, path, path.name)
            file_kind = "svg_reference" if path.name.endswith("_svg.pptx") else "native"
            artifacts["files"].append(
                {
                    "kind": file_kind,
                    "name": path.name,
                    "path": str(exported),
                }
            )
        return artifacts

    @staticmethod
    def _extract_project_path(command_output: str) -> Path:
        for line in command_output.splitlines():
            if line.startswith("Project created:"):
                return Path(line.split("Project created:", 1)[1].strip())
        raise RuntimeError("Unable to parse project path from project_manager output.")

    def _load_style_reference(self, style_objective: str) -> str:
        file_name = STYLE_FILE_MAP.get(style_objective, "executor-consultant.md")
        return (self.references_dir / file_name).read_text(encoding="utf-8")

    @staticmethod
    def _validate_svg(svg_text: str) -> None:
        lowered = svg_text.lower()
        banned = ["<clippath", "<mask", "<style", " class=", "<foreignobject", "<script", "marker-end"]
        for token in banned:
            if token in lowered:
                raise RuntimeError(f"Generated SVG contains banned token: {token}")
        if "<svg" not in lowered:
            raise RuntimeError("Model response did not contain an SVG document.")

    @staticmethod
    def _load_template_reference(project_path: Path, page_role: str) -> str:
        template_dir = project_path / "templates"
        if not template_dir.exists():
            return "free design"
        role_map = {
            "cover": "01_cover.svg",
            "agenda": "02_toc.svg",
            "chapter": "02_chapter.svg",
            "content": "03_content.svg",
            "ending": "04_ending.svg",
        }
        template_name = role_map.get(page_role)
        if not template_name:
            return "free design"
        candidate = template_dir / template_name
        if not candidate.exists():
            return "free design"
        return candidate.read_text(encoding="utf-8")[:6000]
