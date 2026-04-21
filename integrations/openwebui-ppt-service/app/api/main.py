from __future__ import annotations

from pathlib import Path
from typing import Optional

import requests
from fastapi import Depends, FastAPI, File, Form, Header, HTTPException, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, PlainTextResponse

from app.core.job_store import JobStore
from app.core.runtime_config import RuntimeConfigStore
from app.core.settings import Settings, load_settings


SETTINGS = load_settings()
JOB_STORE = JobStore(SETTINGS.storage_dir)
RUNTIME_CONFIG = RuntimeConfigStore(SETTINGS)
APP = FastAPI(title=SETTINGS.app_name)


def get_settings() -> Settings:
    return SETTINGS


def enforce_api_key(
    x_api_key: Optional[str] = Header(default=None),
    settings: Settings = Depends(get_settings),
) -> None:
    runtime_api_key = str(RUNTIME_CONFIG.load().get("service_api_key") or "")
    required_key = runtime_api_key or settings.api_key
    if required_key and x_api_key != required_key:
        raise HTTPException(status_code=401, detail="Invalid API key.")


@APP.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@APP.get("/admin", response_class=HTMLResponse)
def admin_page() -> HTMLResponse:
    html = (Path(__file__).resolve().parents[1] / "templates" / "admin.html").read_text(encoding="utf-8")
    return HTMLResponse(html)


@APP.post("/api/jobs", dependencies=[Depends(enforce_api_key)])
async def create_job(
    project_name: str = Form(...),
    source_text: str = Form(default=""),
    source_url: str = Form(default=""),
    canvas_format: str = Form(default=SETTINGS.default_canvas_format),
    page_count: int = Form(default=SETTINGS.default_page_count),
    target_audience: str = Form(default=""),
    use_case: str = Form(default=""),
    style_objective: str = Form(default=SETTINGS.default_style_objective),
    color_hint: str = Form(default=""),
    image_strategy: str = Form(default=SETTINGS.default_image_strategy),
    icon_style: str = Form(default=SETTINGS.default_icon_style),
    template_name: str = Form(default=""),
    notes_style: str = Form(default="professional"),
    language: str = Form(default=""),
    file: Optional[UploadFile] = File(default=None),
) -> JSONResponse:
    if not any([source_text.strip(), source_url.strip(), file]):
        raise HTTPException(status_code=400, detail="Provide source_text, source_url, or file.")

    payload = {
        "project_name": project_name,
        "source_text": source_text,
        "source_url": source_url,
        "canvas_format": canvas_format,
        "page_count": page_count,
        "target_audience": target_audience,
        "use_case": use_case,
        "style_objective": style_objective,
        "color_hint": color_hint,
        "image_strategy": image_strategy,
        "icon_style": icon_style,
        "template_name": template_name,
        "notes_style": notes_style,
        "language": language,
        "uploaded_file_path": "",
        "uploaded_file_name": "",
    }
    metadata = JOB_STORE.create_job(payload)
    job_paths = JOB_STORE.get_paths(metadata["job_id"])

    if file is not None:
        contents = await file.read()
        if len(contents) > SETTINGS.max_upload_mb * 1024 * 1024:
            raise HTTPException(status_code=400, detail="Uploaded file is too large.")
        destination = job_paths.uploads_dir / file.filename
        destination.write_bytes(contents)
        payload["uploaded_file_path"] = str(destination)
        payload["uploaded_file_name"] = file.filename or destination.name
        metadata = JOB_STORE.update_job(metadata["job_id"], payload=payload)

    return JSONResponse(_public_job_response(metadata))


@APP.post("/api/jobs/json", dependencies=[Depends(enforce_api_key)])
async def create_job_json(body: dict) -> JSONResponse:
    if not any([body.get("source_text", "").strip(), body.get("source_url", "").strip()]):
        raise HTTPException(status_code=400, detail="Provide source_text or source_url.")
    payload = {
        "project_name": body.get("project_name") or "ppt_job",
        "source_text": body.get("source_text", ""),
        "source_url": body.get("source_url", ""),
        "canvas_format": body.get("canvas_format", SETTINGS.default_canvas_format),
        "page_count": int(body.get("page_count", SETTINGS.default_page_count)),
        "target_audience": body.get("target_audience", ""),
        "use_case": body.get("use_case", ""),
        "style_objective": body.get("style_objective", SETTINGS.default_style_objective),
        "color_hint": body.get("color_hint", ""),
        "image_strategy": body.get("image_strategy", SETTINGS.default_image_strategy),
        "icon_style": body.get("icon_style", SETTINGS.default_icon_style),
        "template_name": body.get("template_name", ""),
        "notes_style": body.get("notes_style", "professional"),
        "language": body.get("language", ""),
        "uploaded_file_path": "",
        "uploaded_file_name": "",
    }
    metadata = JOB_STORE.create_job(payload)
    return JSONResponse(_public_job_response(metadata))


@APP.get("/api/jobs/{job_id}", dependencies=[Depends(enforce_api_key)])
def get_job(job_id: str) -> JSONResponse:
    try:
        metadata = JOB_STORE.get_job(job_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Job not found.") from exc
    return JSONResponse(_public_job_response(metadata))


@APP.get("/api/admin/config", dependencies=[Depends(enforce_api_key)])
def get_runtime_config() -> JSONResponse:
    current = RUNTIME_CONFIG.load()
    return JSONResponse(
        {
            "llm_base_url": current.get("llm_base_url", ""),
            "llm_api_key": current.get("llm_api_key", ""),
            "llm_model": current.get("llm_model", ""),
            "ai_image_enabled": bool(current.get("ai_image_enabled", False)),
            "image_backend": current.get("image_backend", "openai"),
            "image_api_key": current.get("image_api_key", ""),
            "image_model": current.get("image_model", ""),
            "image_base_url": current.get("image_base_url", ""),
            "public_base_url": current.get("public_base_url", ""),
            "service_api_key": current.get("service_api_key", ""),
            "default_canvas_format": current.get("default_canvas_format", ""),
            "default_page_count": current.get("default_page_count", 8),
            "default_style_objective": current.get("default_style_objective", ""),
        }
    )


@APP.post("/api/admin/config", dependencies=[Depends(enforce_api_key)])
async def save_runtime_config(body: dict) -> JSONResponse:
    allowed = {
        "llm_base_url",
        "llm_api_key",
        "llm_model",
        "ai_image_enabled",
        "image_backend",
        "image_api_key",
        "image_model",
        "image_base_url",
        "public_base_url",
        "service_api_key",
        "default_canvas_format",
        "default_page_count",
        "default_style_objective",
    }
    payload = {key: value for key, value in body.items() if key in allowed}
    saved = RUNTIME_CONFIG.save(payload)
    return JSONResponse({"ok": True, "config": saved})


@APP.post("/api/admin/llm/models", dependencies=[Depends(enforce_api_key)])
async def fetch_llm_models(body: dict) -> JSONResponse:
    runtime = RUNTIME_CONFIG.load()
    base_url = str(body.get("llm_base_url") or runtime.get("llm_base_url") or "").rstrip("/")
    api_key = str(body.get("llm_api_key") or runtime.get("llm_api_key") or "")
    if not base_url or not api_key:
        raise HTTPException(status_code=400, detail="llm_base_url and llm_api_key are required.")
    response = requests.get(
        f"{base_url}/models",
        headers={"Authorization": f"Bearer {api_key}"},
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()
    models = [
        {"id": item.get("id", ""), "owned_by": item.get("owned_by", "")}
        for item in payload.get("data", [])
        if item.get("id")
    ]
    models.sort(key=lambda item: item["id"])
    return JSONResponse({"models": models})


@APP.post("/api/admin/image/models", dependencies=[Depends(enforce_api_key)])
async def fetch_image_models(body: dict) -> JSONResponse:
    runtime = RUNTIME_CONFIG.load()
    base_url = str(body.get("image_base_url") or runtime.get("image_base_url") or "").rstrip("/")
    api_key = str(body.get("image_api_key") or runtime.get("image_api_key") or "")
    if not base_url or not api_key:
        raise HTTPException(status_code=400, detail="image_base_url and image_api_key are required.")
    response = requests.get(
        f"{base_url}/models",
        headers={"Authorization": f"Bearer {api_key}"},
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()
    models = [
        {"id": item.get("id", ""), "owned_by": item.get("owned_by", "")}
        for item in payload.get("data", [])
        if item.get("id")
    ]
    models.sort(key=lambda item: item["id"])
    return JSONResponse({"models": models})


@APP.get("/api/jobs/{job_id}/logs", dependencies=[Depends(enforce_api_key)])
def get_job_logs(job_id: str) -> PlainTextResponse:
    try:
        logs = JOB_STORE.read_logs(job_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Job not found.") from exc
    return PlainTextResponse(logs)


@APP.get("/api/jobs/{job_id}/artifacts", dependencies=[Depends(enforce_api_key)])
def get_job_artifacts(job_id: str) -> JSONResponse:
    metadata = JOB_STORE.get_job(job_id)
    return JSONResponse(metadata.get("artifacts", {}))


@APP.get("/api/jobs/{job_id}/download/{kind}", dependencies=[Depends(enforce_api_key)])
def download_artifact(job_id: str, kind: str) -> FileResponse:
    metadata = JOB_STORE.get_job(job_id)
    files = metadata.get("artifacts", {}).get("files", [])
    for item in files:
        if item["kind"] == kind:
            path = Path(item["path"])
            return FileResponse(path, filename=path.name)
    raise HTTPException(status_code=404, detail="Artifact not found.")


def _public_job_response(metadata: dict) -> dict:
    job_id = metadata["job_id"]
    runtime_public_base_url = str(RUNTIME_CONFIG.load().get("public_base_url") or "").rstrip("/")
    base_url = runtime_public_base_url or SETTINGS.public_base_url
    response = {
        "job_id": job_id,
        "status": metadata.get("status"),
        "created_at": metadata.get("created_at"),
        "updated_at": metadata.get("updated_at"),
        "error": metadata.get("error"),
        "artifacts": metadata.get("artifacts", {}),
        "links": {
            "self": f"{base_url}/api/jobs/{job_id}",
            "logs": f"{base_url}/api/jobs/{job_id}/logs",
            "artifacts": f"{base_url}/api/jobs/{job_id}/artifacts",
            "download_native": f"{base_url}/api/jobs/{job_id}/download/native",
            "download_svg_reference": f"{base_url}/api/jobs/{job_id}/download/svg_reference",
        },
    }
    return response


app = APP
