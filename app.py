"""Backward-compatible entry point for the original one-file template.

New integrations should import from ``local_biz_ai_assistant`` or use the CLI.
"""

from local_biz_ai_assistant.service import create_service


def generate_business_response(customer_query: str, business_type: str = "Retail Shop") -> str:
    """Return a safe local-mode response while preserving the original API."""

    del business_type  # The configured business profile is now the source of truth.
    return create_service().answer(customer_query).answer


if __name__ == "__main__":
    print(generate_business_response("Aapki dukaan kab tak khuli hai?"))
