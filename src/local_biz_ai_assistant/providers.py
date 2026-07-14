"""Provider-neutral response interface and concrete providers."""

import json
from dataclasses import dataclass
from typing import Protocol

import httpx

from local_biz_ai_assistant.errors import ProviderError
from local_biz_ai_assistant.models import BusinessProfile, Intent, Language


@dataclass(frozen=True)
class ProviderRequest:
    query: str
    profile: BusinessProfile
    intent: Intent
    language: Language
    faq_answer: str | None = None


class ResponseProvider(Protocol):
    name: str

    def respond(self, request: ProviderRequest) -> str:
        """Generate a customer-safe answer."""


class LocalRuleProvider:
    """No-network provider that answers only from validated business data."""

    name = "local"

    def respond(self, request: ProviderRequest) -> str:
        profile = request.profile
        if request.faq_answer:
            return request.faq_answer
        if request.intent == "timings":
            schedule = "; ".join(f"{day}: {hours}" for day, hours in profile.hours.items())
            prefix = (
                "Hamari timings hain" if request.language == "hinglish" else "Our opening hours are"
            )
            return f"{prefix}: {schedule}."
        if request.intent == "location":
            prefix = "Hamara address hai" if request.language == "hinglish" else "Our address is"
            return f"{prefix}: {profile.address}."
        if request.intent == "services":
            services = ", ".join(profile.services)
            prefix = (
                "Hum yeh services offer karte hain"
                if request.language == "hinglish"
                else "We offer"
            )
            return f"{prefix}: {services}."
        if request.intent == "booking":
            if profile.booking_url:
                prefix = "Booking yahan karein" if request.language == "hinglish" else "Book here"
                return f"{prefix}: {profile.booking_url}"
            return _escalation(profile, request.language)
        if request.intent == "contact":
            methods = [
                f"phone: {profile.contact.phone}" if profile.contact.phone else None,
                f"email: {profile.contact.email}" if profile.contact.email else None,
                f"WhatsApp: {profile.contact.whatsapp}" if profile.contact.whatsapp else None,
            ]
            available = [item for item in methods if item]
            if available:
                prefix = (
                    "Aap humein yahan contact kar sakte hain"
                    if request.language == "hinglish"
                    else "Contact us via"
                )
                return f"{prefix}: {', '.join(available)}."
            return _escalation(profile, request.language)
        if request.intent == "pricing":
            prefix = (
                "Exact price service ya product par depend karta hai."
                if request.language == "hinglish"
                else "The exact price depends on the service or product."
            )
            return f"{prefix} {_escalation(profile, request.language)}"
        if request.intent == "greeting":
            if request.language == "hinglish":
                return (
                    f"Namaste! Main {profile.name} ka local assistant hoon. "
                    "Main aapki kya help kar sakta hoon?"
                )
            return f"Hello! I am the local assistant for {profile.name}. How can I help?"
        return _escalation(profile, request.language)


class OpenAICompatibleProvider:
    """Optional adapter for explicitly configured OpenAI-compatible chat APIs."""

    name = "openai-compatible"

    def __init__(
        self,
        *,
        api_key: str,
        base_url: str,
        model: str,
        timeout: float = 15.0,
        transport: httpx.BaseTransport | None = None,
    ):
        self._api_key = api_key
        self._base_url = base_url
        self._model = model
        self._timeout = timeout
        self._transport = transport

    def respond(self, request: ProviderRequest) -> str:
        profile_json = json.dumps(request.profile.model_dump(mode="json"), ensure_ascii=False)
        system = (
            "You are a customer-support assistant. Answer only from the BUSINESS_PROFILE JSON. "
            "Do not invent prices, integrations, policies, or availability. "
            "If the answer is unknown, use the profile's escalation message. "
            "Keep the answer concise and use the requested language. "
            f"BUSINESS_PROFILE={profile_json}"
        )
        payload = {
            "model": self._model,
            "temperature": 0.1,
            "messages": [
                {"role": "system", "content": system},
                {
                    "role": "user",
                    "content": f"Language: {request.language}\nCustomer query: {request.query}",
                },
            ],
        }
        try:
            with httpx.Client(
                timeout=self._timeout, trust_env=False, transport=self._transport
            ) as client:
                response = client.post(
                    f"{self._base_url}/chat/completions",
                    headers={"Authorization": f"Bearer {self._api_key}"},
                    json=payload,
                )
                response.raise_for_status()
                data = response.json()
                answer = data["choices"][0]["message"]["content"]
        except (httpx.HTTPError, KeyError, IndexError, TypeError, ValueError) as exc:
            raise ProviderError(
                "The configured AI provider could not return a valid response. "
                "Try local mode or retry later."
            ) from exc
        if not isinstance(answer, str) or not answer.strip():
            raise ProviderError("The configured AI provider returned an empty response.")
        return answer.strip()[:2000]


def _escalation(profile: BusinessProfile, language: Language) -> str:
    if language == "hinglish":
        return profile.escalation_message_hinglish
    return profile.escalation_message_english
