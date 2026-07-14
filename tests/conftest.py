from collections.abc import Iterator

import pytest

from local_biz_ai_assistant.models import BusinessProfile
from local_biz_ai_assistant.providers import LocalRuleProvider
from local_biz_ai_assistant.service import AssistantService


@pytest.fixture
def profile() -> BusinessProfile:
    return BusinessProfile.model_validate(
        {
            "name": "Sharma Services",
            "description": "Fictional test business",
            "address": "12 Test Road, Delhi",
            "hours": {"Monday-Friday": "09:00-18:00"},
            "services": ["AC repair", "appliance servicing"],
            "faqs": [
                {
                    "question": "Do you offer same-day service?",
                    "answer": "Same-day service is subject to technician availability.",
                }
            ],
            "booking_url": "https://example.invalid/book",
            "contact": {
                "phone": "+91-00000-00000",
                "email": "support@example.invalid",
            },
        }
    )


@pytest.fixture
def service(profile: BusinessProfile) -> Iterator[AssistantService]:
    yield AssistantService(profile=profile, provider=LocalRuleProvider())
