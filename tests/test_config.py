import json
from pathlib import Path

import pytest

from local_biz_ai_assistant.config import load_business_profile, load_settings
from local_biz_ai_assistant.errors import ConfigurationError


def test_default_profile_loads() -> None:
    profile = load_business_profile()
    assert profile.name == "Demo Kirana Store"
    assert profile.services


def test_custom_profile_loads(tmp_path: Path) -> None:
    profile_path = tmp_path / "business.json"
    profile_path.write_text(
        json.dumps(
            {
                "name": "Test Shop",
                "address": "Test Address",
                "hours": {"Daily": "10:00-20:00"},
                "services": ["Repairs"],
            }
        ),
        encoding="utf-8",
    )
    assert load_business_profile(profile_path).name == "Test Shop"


@pytest.mark.parametrize("content", ["not-json", "{}"])
def test_invalid_profile_is_rejected(tmp_path: Path, content: str) -> None:
    profile_path = tmp_path / "broken.json"
    profile_path.write_text(content, encoding="utf-8")
    with pytest.raises(ConfigurationError):
        load_business_profile(profile_path)


def test_missing_profile_is_rejected(tmp_path: Path) -> None:
    with pytest.raises(ConfigurationError, match="not found"):
        load_business_profile(tmp_path / "missing.json")


def test_local_settings_need_no_api_key() -> None:
    settings = load_settings({}, load_env_file=False)
    assert settings.provider == "local"
    assert settings.api_key is None


def test_remote_provider_requires_all_variables() -> None:
    with pytest.raises(ConfigurationError, match="LOCAL_BIZ_API_KEY"):
        load_settings({"LOCAL_BIZ_PROVIDER": "openai-compatible"}, load_env_file=False)


@pytest.mark.parametrize(
    "url",
    [
        "http://provider.example/v1",
        "https://user:password@provider.example/v1",
        "https://provider.example/v1?debug=true",
    ],
)
def test_unsafe_provider_urls_are_rejected(url: str) -> None:
    env = {
        "LOCAL_BIZ_PROVIDER": "openai-compatible",
        "LOCAL_BIZ_API_KEY": "placeholder-not-a-real-secret",
        "LOCAL_BIZ_API_BASE_URL": url,
        "LOCAL_BIZ_MODEL": "example-model",
    }
    with pytest.raises(ConfigurationError):
        load_settings(env, load_env_file=False)


def test_localhost_http_provider_is_allowed() -> None:
    settings = load_settings(
        {
            "LOCAL_BIZ_PROVIDER": "openai-compatible",
            "LOCAL_BIZ_API_KEY": "placeholder-not-a-real-secret",
            "LOCAL_BIZ_API_BASE_URL": "http://127.0.0.1:1234/v1",
            "LOCAL_BIZ_MODEL": "local-model",
        },
        load_env_file=False,
    )
    assert settings.api_base_url == "http://127.0.0.1:1234/v1"


@pytest.mark.parametrize("timeout", ["abc", "0", "61"])
def test_invalid_timeout_is_rejected(timeout: str) -> None:
    with pytest.raises(ConfigurationError):
        load_settings({"LOCAL_BIZ_REQUEST_TIMEOUT": timeout}, load_env_file=False)
