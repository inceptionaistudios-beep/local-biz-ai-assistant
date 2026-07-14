# v0.1.0 — Mock-first Local Business Assistant MVP

Local Business AI Assistant v0.1.0 turns the original two-file template into an installable, testable alpha MVP for Indian micro and small businesses.

## Implemented in this release

- Validated JSON business profiles for name, address, hours, services, FAQs, booking links, and contact details.
- No-key, no-network local mode for common English and basic Roman-script Hinglish questions.
- Deterministic intent handling for timings, location, services, pricing, booking, contact, greetings, FAQs, and human escalation.
- Installable Python 3.10–3.12 package with a `local-biz-ai` CLI.
- FastAPI `GET /health` and `POST /v1/query` endpoints.
- Provider-neutral response interface and an optional, explicitly configured OpenAI-compatible adapter.
- Input, configuration, provider-URL, profile, and request-ID validation.
- Metadata-only request logs that omit customer query text by default.
- Automated tests, coverage enforcement, Ruff, mypy, package builds, dependency auditing, CI, Dependabot, and contributor documentation.

## Installation

```powershell
git clone https://github.com/inceptionaistudios-beep/local-biz-ai-assistant.git
Set-Location local-biz-ai-assistant
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
local-biz-ai ask "Aapki shop kab khuli hai?"
```

No API key is required for the default local mode. See the [README](https://github.com/inceptionaistudios-beep/local-biz-ai-assistant#readme) for Linux/macOS setup, configuration, CLI, and API examples.

## Verification

- 41 automated tests pass on the release candidate.
- Branch coverage is 90.42% with an enforced 85% floor.
- Ruff formatting and lint checks pass.
- Strict mypy checks pass for the source package.
- Source distribution and wheel build successfully.
- Fresh-wheel CLI and loopback API smoke tests pass.
- OSV dependency audit reports no known vulnerabilities at release time.

## Security notes

Local mode makes no external AI-provider request. Secrets belong only in an untracked `.env` file. Remote mode can send the customer query and configured business profile to the selected provider, so consent and provider privacy terms must be reviewed. The API has no authentication or rate limiting and must not be exposed directly to the public internet.

## Known limitations

This is alpha software, not production-ready. Hinglish and FAQ matching are lightweight deterministic baselines. WhatsApp, SMS, CRM, booking-provider synchronization, authentication, rate limiting, persistent storage, multi-tenancy, and hardened deployment are not included. The optional remote adapter is tested with mocked HTTP responses, not paid credentials.

See the [roadmap](https://github.com/inceptionaistudios-beep/local-biz-ai-assistant/blob/main/ROADMAP.md) and [security policy](https://github.com/inceptionaistudios-beep/local-biz-ai-assistant/blob/main/SECURITY.md) before integration or deployment work.
