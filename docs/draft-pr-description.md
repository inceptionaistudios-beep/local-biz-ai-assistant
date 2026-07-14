# Draft Pull Request Description

**Title:** Build a maintainable open-source MVP and contributor foundation

## Summary

This draft PR turns the original two-file placeholder into a mock-first Python alpha MVP. It adds validated business profiles, deterministic English/Hinglish customer support, a CLI, FastAPI endpoints, a provider-neutral interface, an optional OpenAI-compatible adapter, automated tests, packaging, security controls, CI, and complete open-source documentation.

## Motivation

The repository described a useful vision but did not yet provide a configurable package, real integration boundary, tests, dependency metadata, license, or contributor foundation. This change creates the smallest useful implementation while keeping paid credentials and unimplemented messaging channels out of the base path.

## Implementation details

- Added a `src/` package with Pydantic models, JSON configuration, language/intent detection, FAQ matching, safe escalation, providers, service orchestration, CLI, and FastAPI app.
- Preserved `generate_business_response()` through the original `app.py` entry point.
- Added a no-network local provider and a mock-tested OpenAI-compatible adapter.
- Added request-size validation, provider URL validation, bounded request IDs, sanitized errors, and metadata-only logs.
- Added 41 tests covering configuration, English/Hinglish behavior, FAQ routing, escalation, malformed requests, API endpoints, logging, and provider parsing/errors.
- Added packaging, Ruff, mypy, coverage, pip-audit, GitHub Actions, Dependabot, templates, and open-source documentation.

## Files added or changed

- `src/local_biz_ai_assistant/`: application package and fictional built-in profile.
- `tests/`: unit, CLI, provider, configuration, service, and API coverage.
- `examples/`: fictional business profile and sample query dataset.
- `docs/`: architecture, integration boundaries, release draft, application readiness, and GitHub preparation.
- `.github/`: CI, dependency audit, Dependabot, issue forms, and PR template.
- Root project files: README, license, contribution, conduct, security, support, changelog, roadmap, environment example, ignore rules, and package metadata.
- `app.py`: backward-compatible wrapper over the new service.

## Testing performed

- `python -m pytest` — 41 passed; 90.42% coverage.
- `python -m ruff format --check .` — 17 files already formatted.
- `python -m ruff check .` — all checks passed.
- `python -m mypy src` — no issues in 10 source files.
- `python -m build` — sdist and wheel built successfully.
- `python -m pip_audit --local --vulnerability-service osv --progress-spinner off` — no known vulnerabilities found.
- YAML parsing — 6 files valid.
- Markdown link check — 0 missing local links.
- Fresh wheel installation — packaged profile and CLI worked.
- Local API smoke test — health and query endpoints passed on an OS-selected loopback port.

One upstream Starlette TestClient deprecation warning remains; it does not fail the suite.

## Security review

- Scanned the working tree and all 11 local-history commits; no high-confidence secret patterns were found.
- `.env` and common key files are ignored; `.env.example` contains placeholders only.
- Local mode performs no external request.
- Non-local provider URLs require HTTPS except localhost and reject embedded credentials, queries, and fragments.
- Logs omit query text and validate caller-supplied request IDs.
- Sample data is fictional.

## Known limitations

- Alpha MVP; not production-ready.
- No authentication, rate limiting, persistent storage, multi-tenancy, or deployment hardening.
- Hinglish and FAQ matching are lightweight deterministic baselines.
- WhatsApp, SMS, CRM, and booking-provider synchronization are not implemented.
- The optional provider adapter is tested with mock HTTP responses, not paid credentials.
- Remote GitHub Actions status will be known only after this branch is pushed.

## Screenshots or command output

No screenshot is required because the MVP is a CLI/API package. The README includes a generated architecture diagram and exact CLI/API examples. Local verification command results are summarized above.

## Review checklist

- [x] Local mode works without an API key.
- [x] Existing `app.py` entry point remains available.
- [x] Behavior changes have tests.
- [x] Documentation separates completed and planned features.
- [x] No secrets or customer data are included.
- [x] Package data is present in the built wheel.
- [ ] GitHub Actions pass on Python 3.10, 3.11, and 3.12.
- [ ] Maintainer reviews and approves merge.

## Post-merge steps

1. Confirm CI is green on `main`.
2. Refresh the metrics in the OpenAI readiness document.
3. Triage the genuine roadmap issues.
4. Move changelog entries into a dated `0.1.0` section.
5. Follow `docs/release-v0.1.0.md`; publish only after explicit approval.
