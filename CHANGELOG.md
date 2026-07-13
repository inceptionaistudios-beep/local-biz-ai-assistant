# Changelog

All notable project changes will be documented here. The format follows Keep a Changelog principles, and releases will use semantic versioning after maintainer approval.

## [Unreleased]

### Added

- Installable `src/` Python package.
- Validated business profiles and environment configuration.
- No-key local provider with English and basic Hinglish support.
- Provider-neutral interface and optional OpenAI-compatible adapter.
- CLI, health endpoint, and query API.
- Automated unit, API, lint, formatting, type, build, and dependency checks.
- Open-source governance, security, support, architecture, integration, and contribution documentation.

### Changed

- Replaced placeholder-only response behavior with profile-backed deterministic answers.
- Preserved the original `app.py` function as a compatibility wrapper.

### Security

- Reject unsafe remote provider URLs.
- Keep secrets in environment variables and exclude query text from default logs.
- Validate request and profile sizes and formats.

## [0.0.0] - 2026-06-29

### Added

- Initial README and one-file Python template.

[Unreleased]: https://github.com/inceptionaistudios-beep/local-biz-ai-assistant/compare/main...HEAD
