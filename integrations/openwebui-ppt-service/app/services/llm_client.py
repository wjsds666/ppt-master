from __future__ import annotations

import json
import re
import time
from typing import Any

import requests

from app.core.runtime_config import RuntimeConfigStore
from app.core.settings import Settings


class LLMClient:
    def __init__(self, settings: Settings, runtime_config: RuntimeConfigStore) -> None:
        self.settings = settings
        self.runtime_config = runtime_config

    def complete_text(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float | None = None,
    ) -> str:
        runtime = self.runtime_config.load()
        llm_base_url = str(runtime.get("llm_base_url") or self.settings.llm_base_url).rstrip("/")
        llm_api_key = str(runtime.get("llm_api_key") or self.settings.llm_api_key)
        llm_model = str(runtime.get("llm_model") or self.settings.llm_model)
        if not llm_api_key:
            raise RuntimeError("LLM_API_KEY is not configured.")

        payload = {
            "model": llm_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": temperature if temperature is not None else self.settings.llm_temperature,
        }
        last_error: Exception | None = None
        for attempt in range(3):
            try:
                response = requests.post(
                    f"{llm_base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {llm_api_key}",
                        "Content-Type": "application/json",
                    },
                    json=payload,
                    timeout=self.settings.llm_timeout_seconds,
                )
                response.raise_for_status()
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                if isinstance(content, list):
                    return "".join(
                        item.get("text", "") if isinstance(item, dict) else str(item)
                        for item in content
                    )
                return str(content)
            except Exception as exc:  # noqa: BLE001
                last_error = exc
                if attempt < 2:
                    time.sleep(1.2 * (attempt + 1))
                continue
        if last_error is not None:
            raise RuntimeError(f"LLM request failed after retries: {last_error}") from last_error
        raise RuntimeError("LLM request failed after retries.")

    def complete_json(self, system_prompt: str, user_prompt: str) -> dict[str, Any]:
        raw = self.complete_text(system_prompt, user_prompt)
        try:
            return extract_json_object(raw)
        except Exception:  # noqa: BLE001
            repair_prompt = (
                "Return one valid JSON object only. "
                "No markdown fences, no explanations, no prefix, no suffix."
            )
            repaired = self.complete_text(system_prompt, f"{user_prompt}\n\n{repair_prompt}")
            try:
                return extract_json_object(repaired)
            except Exception as exc:  # noqa: BLE001
                snippet = repaired[:300].replace("\n", " ")
                raise RuntimeError(f"LLM JSON parse failed after retry. Snippet: {snippet}") from exc


def extract_json_object(text: str) -> dict[str, Any]:
    fenced = re.search(r"```json\s*(\{.*\})\s*```", text, re.DOTALL)
    candidate = fenced.group(1) if fenced else text.strip()
    if not candidate.startswith("{"):
        start = candidate.find("{")
        end = candidate.rfind("}")
        if start >= 0 and end > start:
            candidate = candidate[start : end + 1]
    return json.loads(candidate)


def extract_code_block(text: str, language: str) -> str:
    pattern = rf"```{language}\s*(.*?)```"
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return text.strip()
