import logging

import pytest

from local_biz_ai_assistant.service import AssistantService


def test_english_timings_query(service: AssistantService) -> None:
    response = service.answer("What are your opening hours?")
    assert response.intent == "timings"
    assert response.language == "english"
    assert "Monday-Friday: 09:00-18:00" in response.answer
    assert not response.escalated


def test_hinglish_timings_query(service: AssistantService) -> None:
    response = service.answer("Aapki dukaan kab khuli hai?")
    assert response.intent == "timings"
    assert response.language == "hinglish"
    assert "Hamari timings" in response.answer


def test_language_can_be_forced(service: AssistantService) -> None:
    response = service.answer("What are your hours?", "hinglish")
    assert response.language == "hinglish"


def test_known_faq_query(service: AssistantService) -> None:
    response = service.answer("Do you offer same-day service?")
    assert response.intent == "faq"
    assert response.answer == "Same-day service is subject to technician availability."


def test_unknown_query_escalates(service: AssistantService) -> None:
    response = service.answer("Can you repair a satellite on Mars?")
    assert response.intent == "escalation"
    assert response.escalated
    assert "not fully sure" in response.answer


@pytest.mark.parametrize("query", ["", "   ", "\n\t"])
def test_blank_query_is_rejected(service: AssistantService, query: str) -> None:
    with pytest.raises(ValueError, match="blank"):
        service.answer(query)


def test_long_query_is_rejected(service: AssistantService) -> None:
    with pytest.raises(ValueError, match="1000"):
        service.answer("x" * 1001)


@pytest.mark.parametrize(
    ("query", "intent", "expected"),
    [
        ("Where are you located?", "location", "12 Test Road"),
        ("What services do you offer?", "services", "AC repair"),
        ("How can I book an appointment?", "booking", "https://example.invalid/book"),
        ("What is your phone number?", "contact", "+91-00000-00000"),
        ("What is the price?", "pricing", "exact price"),
        ("Hello", "greeting", "Sharma Services"),
    ],
)
def test_supported_intents(
    service: AssistantService, query: str, intent: str, expected: str
) -> None:
    response = service.answer(query)
    assert response.intent == intent
    assert expected in response.answer


def test_logs_do_not_include_query(
    service: AssistantService, caplog: pytest.LogCaptureFixture
) -> None:
    customer_query_with_reference = "My customer reference is ABC-123"
    with caplog.at_level(logging.INFO, logger="local_biz_ai_assistant"):
        service.answer(customer_query_with_reference, request_id="safe-request-id")
    assert customer_query_with_reference not in caplog.text
    assert "safe-request-id" in caplog.text
