# GitHub Project Setup Record

Repository metadata, labels, and the genuine issues below were applied on 2026-07-14. Repository security rules were not changed; the remaining main-branch protection work is tracked in [issue #10](https://github.com/inceptionaistudios-beep/local-biz-ai-assistant/issues/10).

## Repository description

Open-source Hinglish and English AI assistant framework for Indian micro and small businesses, featuring local mode, CLI, API, tests, and extensible integration interfaces.

## Accurate topics

`python`, `open-source`, `small-business`, `hinglish`, `customer-support`, `chatbot`, `india`, `automation`, `fastapi`

`whatsapp-integration` is intentionally omitted until a real adapter exists.

## Published genuine issues

- [#2 Expand the reviewed Hinglish intent test dataset](https://github.com/inceptionaistudios-beep/local-biz-ai-assistant/issues/2)
- [#3 Implement a Meta WhatsApp Cloud API adapter](https://github.com/inceptionaistudios-beep/local-biz-ai-assistant/issues/3)
- [#4 Add a booking-provider interface](https://github.com/inceptionaistudios-beep/local-biz-ai-assistant/issues/4)
- [#5 Document authenticated deployment and rate limiting](https://github.com/inceptionaistudios-beep/local-biz-ai-assistant/issues/5)
- [#6 Design privacy-preserving conversation storage](https://github.com/inceptionaistudios-beep/local-biz-ai-assistant/issues/6)
- [#10 Protect main with required CI checks](https://github.com/inceptionaistudios-beep/local-biz-ai-assistant/issues/10)

The sections below retain the original implementation scopes for maintainer reference.

### Expand the reviewed Hinglish intent test dataset

Add fictional Roman-script Hinglish cases for timings, location, services, pricing, booking, contact, greetings, and unknown queries. Document labeling rules, add regression tests, and avoid real customer conversations or personal data.

Acceptance criteria:

- at least 10 reviewed cases per supported intent;
- expected language, intent, and escalation label for each case;
- tests remain deterministic and offline;
- dataset contains fictional data only.

### Implement a Meta WhatsApp Cloud API adapter

Design an optional channel adapter without coupling Meta SDK code to the assistant core. Include webhook signature verification, replay/deduplication handling, sandbox mocks, opt-in/opt-out documentation, sanitized logs, and honest setup limitations.

Acceptance criteria:

- no credentials required for unit tests;
- verified inbound webhook mapping to `QueryRequest`;
- mocked outbound response path;
- retry and duplicate-event tests;
- privacy, cost, and deployment documentation.

### Add a booking-provider interface

Define provider-neutral availability, reservation, cancellation, idempotency, and customer-confirmation contracts. Do not add a provider-specific claim until a sandbox-backed adapter and tests exist.

Acceptance criteria:

- typed interface and error model;
- fake provider for tests;
- idempotency and unavailable-slot cases;
- documentation separating booking links from booking synchronization.

### Add an authenticated deployment and rate-limiting guide

Document one supported deployment path with TLS, API authentication, CORS restrictions, request limits, rate limiting, timeouts, health checks, and secret management. Keep local mode simple and do not claim production readiness from documentation alone.

Acceptance criteria:

- threat-boundary diagram;
- exact configuration examples with placeholders;
- local verification steps;
- rollback and log-sanitization guidance.

### Design privacy-preserving conversation storage

Prepare an opt-in storage design before adding a database. Cover data minimization, consent, tenant separation, encryption, access control, retention, deletion, audit metadata, and the default no-storage behavior.

Acceptance criteria:

- documented data model using fictional examples;
- retention and deletion workflow;
- no raw query logging by default;
- security review before implementation.
