"""Configuration and business-profile loading."""

import json
import os
from collections.abc import Mapping
from dataclasses import dataclass
from importlib.resources import files
from pathlib import Path
from urllib.parse import urlparse

from dotenv import load_dotenv
from pydantic import ValidationError

from local_biz_ai_assistant.errors import ConfigurationError
from local_biz_ai_assistant.models import BusinessProfile

VALID_LOG_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}


@dataclass(frozen=True)
class Settings:
    provider: str = "local"
    profile_path: Path | None = None
    api_key: str | None = None
    api_base_url: str | None = None
    model: str | None = None
    log_level: str = "INFO"
    request_timeout_seconds: float = 15.0


def load_settings(
    environ: Mapping[str, str] | None = None, *, load_env_file: bool = True
) -> Settings:
    if load_env_file:
        load_dotenv(override=False)
    env = os.environ if environ is None else environ
    provider = env.get("LOCAL_BIZ_PROVIDER", "local").strip().lower()
    if provider not in {"local", "openai-compatible"}:
        raise ConfigurationError("LOCAL_BIZ_PROVIDER must be 'local' or 'openai-compatible'.")

    profile_value = env.get("LOCAL_BIZ_PROFILE", "").strip()
    profile_path = Path(profile_value).expanduser() if profile_value else None
    api_key = env.get("LOCAL_BIZ_API_KEY", "").strip() or None
    base_url = env.get("LOCAL_BIZ_API_BASE_URL", "").strip().rstrip("/") or None
    model = env.get("LOCAL_BIZ_MODEL", "").strip() or None
    log_level = env.get("LOCAL_BIZ_LOG_LEVEL", "INFO").strip().upper() or "INFO"
    if log_level not in VALID_LOG_LEVELS:
        allowed = ", ".join(sorted(VALID_LOG_LEVELS))
        raise ConfigurationError(f"LOCAL_BIZ_LOG_LEVEL must be one of: {allowed}.")

    timeout_text = env.get("LOCAL_BIZ_REQUEST_TIMEOUT", "15").strip()
    try:
        timeout = float(timeout_text)
    except ValueError as exc:
        raise ConfigurationError("LOCAL_BIZ_REQUEST_TIMEOUT must be a number.") from exc
    if not 1 <= timeout <= 60:
        raise ConfigurationError("LOCAL_BIZ_REQUEST_TIMEOUT must be between 1 and 60 seconds.")

    if provider == "openai-compatible":
        missing = [
            name
            for name, value in (
                ("LOCAL_BIZ_API_KEY", api_key),
                ("LOCAL_BIZ_API_BASE_URL", base_url),
                ("LOCAL_BIZ_MODEL", model),
            )
            if not value
        ]
        if missing:
            raise ConfigurationError("OpenAI-compatible mode requires: " + ", ".join(missing) + ".")
        _validate_provider_url(base_url or "")

    return Settings(
        provider=provider,
        profile_path=profile_path,
        api_key=api_key,
        api_base_url=base_url,
        model=model,
        log_level=log_level,
        request_timeout_seconds=timeout,
    )


def _validate_provider_url(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme not in {"https", "http"} or not parsed.hostname:
        raise ConfigurationError("LOCAL_BIZ_API_BASE_URL must be a valid HTTP(S) URL.")
    if parsed.scheme == "http" and parsed.hostname not in {"localhost", "127.0.0.1", "::1"}:
        raise ConfigurationError(
            "LOCAL_BIZ_API_BASE_URL must use HTTPS unless the provider is on localhost."
        )
    if parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ConfigurationError(
            "LOCAL_BIZ_API_BASE_URL must not contain credentials, a query, or a fragment."
        )


def load_business_profile(path: Path | None = None) -> BusinessProfile:
    try:
        if path is None:
            raw = (
                files("local_biz_ai_assistant")
                .joinpath("data/default_business.json")
                .read_text(encoding="utf-8")
            )
        else:
            raw = path.read_text(encoding="utf-8")
        payload = json.loads(raw)
        return BusinessProfile.model_validate(payload)
    except FileNotFoundError as exc:
        raise ConfigurationError(f"Business profile was not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ConfigurationError("Business profile must contain valid JSON.") from exc
    except ValidationError as exc:
        fields = sorted({str(item["loc"][0]) for item in exc.errors() if item["loc"]})
        suffix = f" Check: {', '.join(fields)}." if fields else ""
        raise ConfigurationError("Business profile validation failed." + suffix) from exc
