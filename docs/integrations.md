# Integration Guide

## Current status

| Integration | Status |
| --- | --- |
| CLI | Implemented and tested |
| Local HTTP API | Implemented and tested |
| Local deterministic provider | Implemented and tested |
| OpenAI-compatible provider | Implemented; HTTP behavior tested with a mock transport, not live paid credentials |
| Website widget | Not implemented |
| Meta WhatsApp Cloud API | Not implemented |
| Twilio WhatsApp or SMS | Not implemented |
| Indian SMS gateways | Not implemented |
| CRM | Not implemented |
| Booking-provider synchronization | Not implemented |

## HTTP contract for future channels

Adapters can call:

```http
POST /v1/query
Content-Type: application/json
X-Request-ID: channel-generated-id

{"query":"What are your timings?","language":"auto"}
```

The response contains `answer`, `intent`, `language`, `provider`, `escalated`, and `request_id`. An adapter should preserve the request ID for debugging without logging the message body.

## Channel adapter checklist

Before calling a messaging integration complete:

1. Verify webhook signatures and reject replayed or stale events.
2. Map provider-specific identifiers without exposing phone numbers in logs.
3. Enforce authentication, rate limits, request-size limits, and timeouts.
4. Obtain consent and document opt-out behavior for any outbound message.
5. Deduplicate webhook retries.
6. Mock the external API in automated tests.
7. Test a sandbox or test number using non-customer data.
8. Document costs, credential scopes, data retention, and deletion.
9. Keep auto-send behavior disabled unless the integration explicitly requires it and has safety controls.

## Website integration

A website can call the API only through a trusted backend. Do not put `LOCAL_BIZ_API_KEY` or any provider token in browser JavaScript. A public deployment also needs authentication or abuse controls, TLS, CORS restrictions, rate limiting, and monitoring.

## OpenAI-compatible providers

The optional adapter sends a chat-completions request to `{LOCAL_BIZ_API_BASE_URL}/chat/completions`. Compatibility varies between providers. The project does not currently certify OpenAI, OpenRouter, BluesMinds, Gemini, Anthropic, or any other service. Add provider-specific documentation only after a sandbox or mock-backed adapter exists.

## Booking and CRM

The current `booking_url` is a customer-facing link, not synchronization. A future booking interface should separate availability lookup, reservation creation, cancellation, idempotency, and user confirmation. CRM integrations should minimize stored data and define deletion and retention behavior before implementation.
