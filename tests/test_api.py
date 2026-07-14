from fastapi.testclient import TestClient

from local_biz_ai_assistant.api import create_app
from local_biz_ai_assistant.service import AssistantService


def test_health_endpoint(service: AssistantService) -> None:
    client = TestClient(create_app(service))
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "mode": "local",
        "business": "Sharma Services",
        "version": "0.1.0",
    }


def test_query_endpoint(service: AssistantService) -> None:
    client = TestClient(create_app(service))
    response = client.post(
        "/v1/query",
        headers={"X-Request-ID": "test-request"},
        json={"query": "Aap kahan located hain?", "language": "auto"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["intent"] == "location"
    assert payload["language"] == "hinglish"
    assert payload["request_id"] == "test-request"


def test_malformed_request_is_rejected(service: AssistantService) -> None:
    client = TestClient(create_app(service))
    assert client.post("/v1/query", json={}).status_code == 422
    assert client.post("/v1/query", json={"query": "   "}).status_code == 422
    assert client.post("/v1/query", json={"query": "x" * 1001}).status_code == 422
    assert client.post("/v1/query", json={"query": "hello", "language": "Hindi"}).status_code == 422


def test_unsafe_request_id_is_replaced(service: AssistantService) -> None:
    client = TestClient(create_app(service))
    response = client.post(
        "/v1/query",
        headers={"X-Request-ID": "not safe because it has spaces"},
        json={"query": "hello"},
    )
    assert response.status_code == 200
    assert response.json()["request_id"] != "not safe because it has spaces"
    assert len(response.json()["request_id"]) == 32
