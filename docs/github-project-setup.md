# GitHub Project Setup Drafts

No settings or issues described here have been published yet.

## Repository description

Mock-first Python framework for English/Hinglish small-business customer support, with CLI, FastAPI, tests, and safe extension points.

## Accurate topics

`python`, `open-source`, `small-business`, `hinglish`, `customer-support`, `chatbot`, `india`, `automation`

`whatsapp-integration` is intentionally omitted until a real adapter exists.

## Genuine issue drafts

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
