# -*- coding: utf-8 -*-

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(*args, **kwargs) -> bool:
        return False


class GeminiConfigurationError(RuntimeError):
    pass


@dataclass(frozen=True)
class GeminiSettings:
    api_keys: tuple[str, ...] = field(default_factory=tuple)
    model: str = "gemini-3.1-flash-lite"
    temperature: float = 0.3


class GeminiClient:
    def __init__(self, settings: GeminiSettings | None = None):
        env_path = Path(__file__).resolve().parents[2] / ".env"
        load_dotenv(dotenv_path=env_path)
        self.settings = settings or GeminiSettings(
            api_keys=self._load_api_keys(),
            model=os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite").strip() or "gemini-3.1-flash-lite",
            temperature=float(os.getenv("GEMINI_TEMPERATURE", "0.3")),
        )

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        if not self.settings.api_keys:
            raise GeminiConfigurationError(
                "Nenhuma chave Gemini configurada. Defina GEMINI_API_KEY, GEMINI_API_KEYS ou GEMINI_API_KEY_1."
            )

        try:
            from google import genai
            from google.genai import types
        except ImportError as error:
            raise GeminiConfigurationError(
                "Pacote google-genai não está instalado. Execute: pip install google-genai"
            ) from error

        errors: list[str] = []
        for index, api_key in enumerate(self.settings.api_keys, start=1):
            client = genai.Client(api_key=api_key)
            try:
                response = client.models.generate_content(
                    model=self.settings.model,
                    contents=user_prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=system_prompt,
                        temperature=self.settings.temperature,
                    ),
                )
                text = getattr(response, "text", "") or ""
                return text.strip() or "Não encontrei informações suficientes para responder com segurança."
            except Exception as error:
                message = str(error)
                errors.append(f"chave {index}: {message}")
                if not self._should_try_next_key(message):
                    break

        raise RuntimeError(
            f"Falha ao consultar Gemini com o modelo {self.settings.model}. "
            f"Tentativas: {' | '.join(errors)}"
        )

    def _load_api_keys(self) -> tuple[str, ...]:
        raw_keys: list[str] = []
        raw_keys.extend(self._split_keys(os.getenv("GEMINI_API_KEYS", "")))
        for index in range(1, 4):
            raw_keys.extend(self._split_keys(os.getenv(f"GEMINI_API_KEY_{index}", "")))
        raw_keys.extend(self._split_keys(os.getenv("GEMINI_API_KEY", "")))

        unique_keys: list[str] = []
        seen: set[str] = set()
        for key in raw_keys:
            if key and key not in seen:
                unique_keys.append(key)
                seen.add(key)
        return tuple(unique_keys)

    def _split_keys(self, value: str) -> list[str]:
        return [item.strip() for item in value.replace("\n", ",").split(",") if item.strip()]

    def _should_try_next_key(self, message: str) -> bool:
        lowered = message.lower()
        retry_markers = (
            "429",
            "resource_exhausted",
            "quota",
            "rate",
            "limit",
            "503",
            "unavailable",
            "high demand",
            "api key not valid",
            "permission_denied",
            "unauthorized",
            "forbidden",
        )
        return any(marker in lowered for marker in retry_markers)
