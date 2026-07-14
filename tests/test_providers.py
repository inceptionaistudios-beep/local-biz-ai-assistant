import json

import httpx
import pytest

from local_biz_ai_assistant.errors import ProviderError
from local_biz_ai_assistant.models import BusinessProfile
from local_biz_ai_assistant.providers import OpenAICompatibleProvider, ProviderRequest


def make_request(profile: BusinessProfile) -> ProviderRequest:
    return ProviderRequest(
        query="What are your hours?",
        profile=profile,
        intent="timings",
        language="english",
    )


def test_openai_compatible_provider_parses_response(profile: BusinessProfile) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["Authorization"] == "Bearer placeholder-key"
        payload = json.loads(request.content)
        assert payload["model"] == "test-model"
        return httpx.Response(200, json={"choices": [{"message": {"content": "We open at 9 AM."}}]})

    provider = OpenAICompatibleProvider(
        api_key="placeholder-key",
        base_url="https://provider.example/v1",
        model="test-model",
        transport=httpx.MockTransport(handler),
    )
    assert provider.respond(make_request(profile)) == "We open at 9 AM."


@pytest.mark.parametrize(
    "response",
    [httpx.Response(500), httpx.Response(200, json={"unexpected": "shape"})],
)
def test_openai_compatible_provider_fails_safely(
    profile: BusinessProfile, response: httpx.Response
) -> None:
    provider = OpenAICompatibleProvider(
        api_key="secret-must-not-appear",
        base_url="https://provider.example/v1",
        model="test-model",
        transport=httpx.MockTransport(lambda _: response),
    )
    with pytest.raises(ProviderError) as caught:
        provider.respond(make_request(profile))
    assert "secret-must-not-appear" not in str(caught.value)
