"""FastAPI application for website and channel adapters."""

from fastapi import FastAPI, HTTPException, Request

from local_biz_ai_assistant import __version__
from local_biz_ai_assistant.errors import ConfigurationError, ProviderError
from local_biz_ai_assistant.models import AssistantResponse, HealthResponse, QueryRequest
from local_biz_ai_assistant.service import AssistantService, create_service


def create_app(service: AssistantService | None = None) -> FastAPI:
    selected_service = service or create_service()
    application = FastAPI(
        title="Local Business AI Assistant",
        version=__version__,
        description="Mock-first Hinglish and English customer-support API.",
    )

    @application.get("/health", response_model=HealthResponse, tags=["system"])
    def health() -> HealthResponse:
        return HealthResponse(
            mode=selected_service.provider.name,
            business=selected_service.profile.name,
            version=__version__,
        )

    @application.post("/v1/query", response_model=AssistantResponse, tags=["assistant"])
    def query(payload: QueryRequest, request: Request) -> AssistantResponse:
        request_id = request.headers.get("X-Request-ID")
        try:
            return selected_service.answer(payload.query, payload.language, request_id=request_id)
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        except ProviderError as exc:
            raise HTTPException(status_code=502, detail=str(exc)) from exc

    return application


try:
    app = create_app()
except ConfigurationError as exc:
    raise RuntimeError(f"Application configuration error: {exc}") from exc
