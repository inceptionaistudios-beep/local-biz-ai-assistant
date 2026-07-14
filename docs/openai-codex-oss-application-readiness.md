# OpenAI Codex for Open Source Application Readiness

This is a truthful preparation document, not an application submission or eligibility claim.

## Repository and maintainer

- Repository: https://github.com/inceptionaistudios-beep/local-biz-ai-assistant
- Maintainer: Aarav Kumar Katiyar
- Role: Founder, CEO, and Chief Developer of InceptionAIStudios; public repository maintainer
- License: MIT

## Public evidence snapshot

- Final `main` commit for v0.1.0: `f8eb821dba3a207074257cf0c89fef20f887aeb9`
- MVP pull request: https://github.com/inceptionaistudios-beep/local-biz-ai-assistant/pull/1
- Main CI: https://github.com/inceptionaistudios-beep/local-biz-ai-assistant/actions/runs/29358526682
- Dependency security: https://github.com/inceptionaistudios-beep/local-biz-ai-assistant/actions/runs/29359072654
- Release: https://github.com/inceptionaistudios-beep/local-biz-ai-assistant/releases/tag/v0.1.0

## Project purpose

The project is a lightweight, mock-first Python framework for Indian micro and small businesses to answer repeated customer questions in English and simple Hinglish. It is intended as an open-source foundation for future website and messaging-channel adapters without requiring a paid AI API for the base experience.

## Implemented features

- Installable Python package and backward-compatible `app.py` entry point.
- Validated business-profile JSON and environment settings.
- No-key, no-network deterministic local mode.
- Basic intent detection, English/Hinglish selection, FAQ matching, and human escalation.
- CLI and FastAPI health/query endpoints.
- Provider-neutral protocol and optional OpenAI-compatible adapter.
- Secret-safe configuration, provider URL checks, input validation, and metadata-only logs.
- Automated unit and API tests plus lint, format, type, build, and dependency checks.

## Tests and CI

The final local readiness run on 2026-07-14 uses Python 3.12, pytest 9.1.1, pytest-cov 7.1.0, and mypy 2.3.0. All 41 tests pass with 90.42% branch coverage and an enforced 85% floor. Tests cover configuration, missing provider variables, English and Hinglish queries, FAQs, escalation, malformed input, API endpoints, provider response parsing, and safe errors.

GitHub Actions passed on `main` for Python 3.10, 3.11, and 3.12. Ruff, strict mypy, package build, and OSV dependency-audit checks also passed without private secrets.

## Maintenance responsibilities

Aarav is responsible for public issue triage, reviewing community pull requests, keeping tests and documentation accurate, coordinating security fixes, checking dependency updates, and approving releases. The repository's public maintenance process is separate from private InceptionAIStudios client work.

## Ecosystem value

The repository offers a small, inspectable baseline for contributors interested in Indian small-business support, Roman-script Hinglish, privacy-aware local operation, and channel-agnostic integration design. It can help contributors learn from a real but deliberately limited Python service instead of a placeholder or fabricated integration demo.

## GitHub metrics snapshot

Public repository and API snapshot on 2026-07-14 after v0.1.0 publication:

- Stars: 0
- Forks: 0
- Open issues: 6 genuine roadmap or governance issues
- Open pull requests: 0
- Published releases: 1 (`v0.1.0`)
- Commits on `main`: 23
- Commit contributors returned by GitHub: 1 human maintainer and Dependabot bot
- External human contributors: 0
- Release-asset downloads: not applicable because no binary assets were uploaded; GitHub does not expose source-archive download counts

These metrics must be refreshed immediately before any future application submission. No adoption, user, customer, source-download, or installation count is claimed.

## Current limitations

- Alpha MVP; not production-ready.
- Keyword-based Hinglish support and lightweight FAQ matching.
- No authentication, rate limiting, storage, multi-tenancy, or production deployment.
- No implemented WhatsApp, SMS, CRM, or booking-provider adapter.
- Optional remote adapter tested with mocked HTTP responses, not paid credentials.
- The `main` branch is not yet protected by a required-check ruleset; this is tracked in issue #10.
- No confirmed public users, installations, source-download count, or external human contributors.

## Planned maintenance workflow

- Require tests, Ruff, mypy, build checks, and dependency audit on pull requests.
- Review Dependabot updates rather than auto-merging them.
- Use focused issues for roadmap work.
- Keep completed and planned features separate in README, changelog, and roadmap.
- Prepare releases through a checklist and require maintainer approval.
- Handle vulnerabilities privately and add regression tests with fixes.

## Proposed use of Codex and possible API credits

Codex would support public maintenance work: issue reproduction, test generation and review, documentation consistency, contributor onboarding, code review assistance, and safe adapter prototyping. Possible API credits would fund public, opt-in evaluation tooling and test-data generation using fictional or consent-safe prompts. They would not be used for private paid InceptionAIStudios client projects.

## Suggested form responses

Each response below is under 500 characters.

### 1. Why does this repository qualify?

Local Business AI Assistant is a public MIT-licensed Python MVP for Indian micro and small businesses. It provides a no-key local mode, English/Hinglish intent handling, validated business profiles, CLI/API access, tests, CI, and honest integration boundaries. I maintain its public issues, reviews, security fixes, documentation, and releases separately from private InceptionAIStudios client work.

### 2. How will you use API credits for your project?

Credits would support only this public open-source project: opt-in evaluation tools, fictional Hinglish test-data generation, regression testing, documentation examples, and safe prototypes for community-reviewed adapters. They would not fund private paid InceptionAIStudios client work, production customer traffic, unsolicited messaging, or hidden commercial integrations.

### 3. Anything else we should know?

The project is early: v0.1.0 is public, with 0 stars, 0 forks, no claimed users or installations, and no external human contributors. Completed features remain separate from six genuine roadmap/governance issues. Codex would help a student maintainer reproduce issues, review contributions, improve tests and docs, and preserve security boundaries as the project grows through genuine work.
