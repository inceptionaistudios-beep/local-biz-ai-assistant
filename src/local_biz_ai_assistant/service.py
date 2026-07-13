"""Application service that coordinates validation, intent detection, and providers."""

import logging
import re
from uuid import uuid4

from local_biz_ai_assistant.config import Settings, load_business_profile, load_settings
from local_biz_ai_assistant.intent import detect_intent, detect_language, find_matching_faq
from local_biz_ai_assistant.models import (
    AssistantResponse,
    BusinessProfile,
    RequestedLanguage,
)
from local_biz_ai_assistant.providers import (
    LocalRuleProvider,
    OpenAICompatibleProvider,
    ProviderRequest,
    ResponseProvider,
)

LOGGER = logging.getLogger("local_biz_ai_assistant")
REQUEST_ID_PATTERN = re.compile(r"^[A-Za-z0-9._:-]{1,64}$")


class AssistantService:
    def __init__(self, *, profile: BusinessProfile, provider: ResponseProvider):
        self.profile = profile
        self.provider = provider

    def answer(
        self, query: str, language: RequestedLanguage = "auto", *, request_id: str | None = None
    ) -> AssistantResponse:
        cleaned = query.strip()
        if not cleaned:
            raise ValueError("Query must not be blank.")
        if len(cleaned) > 1000:
            raise ValueError("Query must be 1000 characters or fewer.")

        selected_language = detect_language(cleaned) if language == "auto" else language
        faq = find_matching_faq(cleaned, self.profile)
        intent = "faq" if faq else detect_intent(cleaned)
        effective_intent = "escalation" if intent == "faq" and faq is None else intent
        event_id = (
            request_id if request_id and REQUEST_ID_PATTERN.fullmatch(request_id) else uuid4().hex
        )
        provider_request = ProviderRequest(
            query=cleaned,
            profile=self.profile,
            intent=effective_intent,
            language=selected_language,
            faq_answer=faq.answer if faq else None,
        )
        answer = self.provider.respond(provider_request)
        escalated = effective_intent == "escalation" or (
            effective_intent in {"booking", "contact"}
            and (
                (effective_intent == "booking" and not self.profile.booking_url)
                or (
                    effective_intent == "contact"
                    and not any(
                        [
                            self.profile.contact.phone,
                            self.profile.contact.email,
                            self.profile.contact.whatsapp,
                        ]
                    )
                )
            )
        )
        LOGGER.info(
            "request_completed request_id=%s intent=%s language=%s provider=%s escalated=%s",
            event_id,
            effective_intent,
            selected_language,
            self.provider.name,
            escalated,
        )
        return AssistantResponse(
            answer=answer,
            intent=effective_intent,
            language=selected_language,
            provider=self.provider.name,
            escalated=escalated,
            request_id=event_id,
        )


def create_service(
    settings: Settings | None = None, profile: BusinessProfile | None = None
) -> AssistantService:
    selected_settings = settings or load_settings()
    selected_profile = profile or load_business_profile(selected_settings.profile_path)
    if selected_settings.provider == "local":
        provider: ResponseProvider = LocalRuleProvider()
    else:
        provider = OpenAICompatibleProvider(
            api_key=selected_settings.api_key or "",
            base_url=selected_settings.api_base_url or "",
            model=selected_settings.model or "",
            timeout=selected_settings.request_timeout_seconds,
        )
    logging.basicConfig(
        level=getattr(logging, selected_settings.log_level, logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    return AssistantService(profile=selected_profile, provider=provider)
