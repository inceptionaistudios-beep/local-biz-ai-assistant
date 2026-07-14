# v0.1.0 Release Runbook

This is the maintainer checklist for the authorised v0.1.0 publication run. The release must still be created only from a green, verified `main` commit. Public release notes are maintained in [release-notes-v0.1.0.md](release-notes-v0.1.0.md).

## Release title

v0.1.0 — Mock-first Local Business Assistant MVP

## Release summary

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

- [x] Pull request #1 reviewed and merged by Aarav.
- [x] CI green on `main` for Python 3.10-3.12.
- [x] Fresh-wheel installation and local CLI/API smoke tests pass.
- [x] Full local diff and secret scan reviewed.
- [x] `CHANGELOG.md` moves release items into the dated `0.1.0` section.
- [x] Package version and Git tag both equal `0.1.0` / `v0.1.0`.
- [x] Release notes rechecked for truthful feature claims.
- [x] Tag created from the intended `main` commit (`f8eb821d`).
- [x] Aarav authorised v0.1.0 publication in the final completion run.
- [x] GitHub release and tag are publicly verified after publication.

## Published evidence

- Release: https://github.com/inceptionaistudios-beep/local-biz-ai-assistant/releases/tag/v0.1.0
- Tag target: `f8eb821dba3a207074257cf0c89fef20f887aeb9`
- Main CI: https://github.com/inceptionaistudios-beep/local-biz-ai-assistant/actions/runs/29358526682
- Dependency security: https://github.com/inceptionaistudios-beep/local-biz-ai-assistant/actions/runs/29359072654

## Commands used for the release

Run only after the pull request is reviewed, all required checks pass, and the PR is merged:

```powershell
git switch main
git pull --ff-only origin main
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m ruff format --check .
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m mypy src
.\.venv\Scripts\python.exe -m build
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin v0.1.0
gh release create v0.1.0 --title "v0.1.0 — Mock-first Local Business Assistant MVP" --notes-file docs/release-notes-v0.1.0.md
```

After publication, verify the tag, release page, release notes, target commit, and `main` CI. Do not mark the project as production-ready.
