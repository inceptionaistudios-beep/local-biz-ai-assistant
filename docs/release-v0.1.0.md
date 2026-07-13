# Proposed v0.1.0 Release

No release has been published. This document is a maintainer draft for approval.

## Draft title

v0.1.0 — Mock-first Local Business Assistant MVP

## Draft release notes

Local Business AI Assistant v0.1.0 turns the original two-file template into an installable, testable alpha MVP for Indian micro and small businesses.

### Highlights

- Configure business name, address, hours, services, FAQs, booking link, and contact details in JSON.
- Answer common English and basic Roman-script Hinglish questions in no-key local mode.
- Use a CLI or FastAPI health/query endpoints.
- Extend the provider-neutral interface; optionally use an explicitly configured OpenAI-compatible endpoint.
- Validate profiles, environment variables, request length, and provider URLs.
- Avoid logging customer query text by default.
- Run automated tests, Ruff, mypy, package builds, and dependency auditing.
- Use new contribution, security, support, architecture, integration, and roadmap documentation.

### Important limitations

This is alpha software, not production-ready. WhatsApp, SMS, CRM, booking synchronization, authentication, rate limiting, persistent storage, and deployment hardening are not included. The OpenAI-compatible adapter is tested with mocked HTTP responses, not paid credentials.

### Upgrade note

The original `generate_business_response()` function remains available through `app.py`, but business facts now come from the validated profile.

## Release checklist

- [ ] Draft PR approved and merged by Aarav.
- [ ] CI green on `main` for Python 3.10-3.12.
- [ ] Fresh clone installation and local smoke test pass.
- [ ] Full diff and secret scan reviewed.
- [ ] `CHANGELOG.md` moves Unreleased items into a dated `0.1.0` section.
- [ ] Package version and Git tag both equal `0.1.0` / `v0.1.0`.
- [ ] Release notes rechecked for truthful feature claims.
- [ ] Tag created from the intended `main` commit.
- [ ] GitHub release created only after Aarav's explicit approval.

## Exact post-approval commands

Run only after the draft PR is reviewed, approved, and merged:

```powershell
git switch main
git pull --ff-only origin main
python -m pytest
python -m ruff format --check .
python -m ruff check .
python -m mypy src
python -m build
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin v0.1.0
```

Then create a GitHub release from tag `v0.1.0`, paste the reviewed notes above, and publish only with explicit final approval. Do not mark it as production-ready.
