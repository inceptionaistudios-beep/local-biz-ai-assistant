"""Validated data models used by the assistant."""

from typing import Literal

from pydantic import BaseModel, Field, HttpUrl, field_validator

Language = Literal["english", "hinglish"]
RequestedLanguage = Literal["auto", "english", "hinglish"]
Intent = Literal[
    "timings",
    "location",
    "services",
    "pricing",
    "booking",
    "contact",
    "greeting",
    "faq",
    "escalation",
]


class ContactDetails(BaseModel):
    phone: str | None = Field(default=None, max_length=40)
    email: str | None = Field(default=None, max_length=254)
    whatsapp: str | None = Field(default=None, max_length=40)


class FAQ(BaseModel):
    question: str = Field(min_length=2, max_length=300)
    answer: str = Field(min_length=2, max_length=1500)


class BusinessProfile(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    description: str = Field(default="", max_length=500)
    address: str = Field(min_length=2, max_length=500)
    hours: dict[str, str] = Field(min_length=1)
    services: list[str] = Field(min_length=1, max_length=50)
    faqs: list[FAQ] = Field(default_factory=list, max_length=100)
    booking_url: HttpUrl | None = None
    contact: ContactDetails = Field(default_factory=ContactDetails)
    currency: str = Field(default="INR", min_length=3, max_length=3)
    escalation_message_english: str = Field(
        default="I am not fully sure about that. Please contact our team for a confirmed answer.",
        min_length=5,
        max_length=500,
    )
    escalation_message_hinglish: str = Field(
        default=(
            "Mujhe iski pakki jankari nahi hai. Confirm answer ke liye "
            "hamari team se contact karein."
        ),
        min_length=5,
        max_length=500,
    )

    @field_validator("name", "address")
    @classmethod
    def strip_required_text(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("must not be blank")
        return cleaned

    @field_validator("hours")
    @classmethod
    def clean_hours(cls, value: dict[str, str]) -> dict[str, str]:
        cleaned: dict[str, str] = {}
        for day, hours in value.items():
            clean_day = day.strip()
            clean_value = hours.strip()
            if not clean_day or not clean_value:
                raise ValueError("hours must use non-blank day and schedule values")
            cleaned[clean_day] = clean_value
        return cleaned

    @field_validator("services")
    @classmethod
    def clean_services(cls, value: list[str]) -> list[str]:
        cleaned = [item.strip() for item in value if item.strip()]
        if not cleaned:
            raise ValueError("must contain at least one non-empty service")
        return cleaned


class QueryRequest(BaseModel):
    query: str = Field(min_length=1, max_length=1000)
    language: RequestedLanguage = "auto"

    @field_validator("query")
    @classmethod
    def reject_blank_query(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("query must not be blank")
        return cleaned


class AssistantResponse(BaseModel):
    answer: str
    intent: Intent
    language: Language
    provider: str
    escalated: bool
    request_id: str


class HealthResponse(BaseModel):
    status: Literal["ok"] = "ok"
    mode: str
    business: str
    version: str
