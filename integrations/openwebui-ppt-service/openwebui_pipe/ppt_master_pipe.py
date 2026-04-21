"""
OpenWebUI Pipe for the standalone PPT Master service.

Import this file in OpenWebUI Functions -> Import.
"""

from __future__ import annotations

import json
import time
from typing import Any

import requests
from pydantic import BaseModel, Field


class Pipe:
    class Valves(BaseModel):
        service_url: str = Field(default="http://127.0.0.1:8099", description="PPT service base URL")
        service_api_key: str = Field(default="", description="SERVICE_API_KEY for the PPT service")
        canvas_format: str = Field(default="ppt169", description="Default canvas format")
        page_count: int = Field(default=8, description="Default page count")
        style_objective: str = Field(
            default="general_consulting",
            description="general_versatile or general_consulting or top_consulting",
        )
        poll_interval_seconds: int = Field(default=5, description="Polling interval")
        max_wait_seconds: int = Field(default=900, description="Maximum wait time before returning a pending job")

    def __init__(self) -> None:
        self.valves = self.Valves()

    def pipes(self) -> list[dict[str, str]]:
        return [{"id": "ppt-master-service", "name": "PPT Master Service"}]

    async def pipe(
        self,
        body: dict[str, Any],
        __event_emitter__=None,
        __user__=None,
    ) -> str:
        prompt = self._last_user_message(body)
        if not prompt:
            return "Please provide the source material or requirements for the PPT."

        if __event_emitter__:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {"description": "Submitting PPT generation job...", "done": False},
                }
            )

        headers = {"Content-Type": "application/json"}
        if self.valves.service_api_key:
            headers["X-API-Key"] = self.valves.service_api_key

        create_resp = requests.post(
            f"{self.valves.service_url}/api/jobs/json",
            headers=headers,
            json={
                "project_name": "openwebui_ppt",
                "source_text": prompt,
                "canvas_format": self.valves.canvas_format,
                "page_count": self.valves.page_count,
                "style_objective": self.valves.style_objective,
            },
            timeout=60,
        )
        create_resp.raise_for_status()
        job = create_resp.json()
        job_id = job["job_id"]

        deadline = time.time() + self.valves.max_wait_seconds
        while time.time() < deadline:
            time.sleep(self.valves.poll_interval_seconds)
            status_resp = requests.get(
                f"{self.valves.service_url}/api/jobs/{job_id}",
                headers=headers,
                timeout=60,
            )
            status_resp.raise_for_status()
            status = status_resp.json()
            if __event_emitter__:
                await __event_emitter__(
                    {
                        "type": "status",
                        "data": {
                            "description": f"PPT job {job_id} is {status['status']}",
                            "done": False,
                        },
                    }
                )
            if status["status"] == "succeeded":
                if __event_emitter__:
                    await __event_emitter__(
                        {
                            "type": "status",
                            "data": {"description": "PPT generation finished.", "done": True},
                        }
                    )
                return self._render_success(status)
            if status["status"] == "failed":
                return f"PPT generation failed.\n\nJob ID: `{job_id}`\nError: {status.get('error', 'unknown error')}"

        return (
            "PPT job is still running.\n\n"
            f"Job ID: `{job_id}`\n"
            f"Status: `{job['status']}`\n"
            f"Track: {job['links']['self']}\n"
            f"Logs: {job['links']['logs']}"
        )

    @staticmethod
    def _last_user_message(body: dict[str, Any]) -> str:
        messages = body.get("messages", [])
        for message in reversed(messages):
            if message.get("role") != "user":
                continue
            content = message.get("content", "")
            if isinstance(content, list):
                text_parts = []
                for item in content:
                    if isinstance(item, dict) and item.get("type") == "text":
                        text_parts.append(item.get("text", ""))
                return "\n".join(part for part in text_parts if part).strip()
            return str(content).strip()
        return ""

    @staticmethod
    def _render_success(status: dict[str, Any]) -> str:
        files = status.get("artifacts", {}).get("files", [])
        rows = [f"Job ID: `{status['job_id']}`", ""]
        for item in files:
            rows.append(f"- {item['kind']}: {item['name']}")
        rows.append("")
        rows.append(f"Native PPTX: {status['links']['download_native']}")
        rows.append(f"SVG Reference PPTX: {status['links']['download_svg_reference']}")
        rows.append(f"Logs: {status['links']['logs']}")
        return "\n".join(rows)
