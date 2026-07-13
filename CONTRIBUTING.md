# Contributing

Thank you for helping improve Local Business AI Assistant.

## Good first contributions

- Add tests for real Hinglish phrasing without adding personal data.
- Improve error messages or documentation.
- Add a business-profile validation case.
- Propose a channel adapter interface with mocks and no credentials.

## Development setup

```powershell
git clone https://github.com/inceptionaistudios-beep/local-biz-ai-assistant.git
Set-Location local-biz-ai-assistant
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
python -m pytest
```

On macOS or Linux, activate with `source .venv/bin/activate`.

## Workflow

1. Search existing issues and pull requests.
2. Open an issue for large changes or integrations.
3. Create a focused branch from `main`.
4. Add or update tests for behavior changes.
5. Run all local checks listed in the README.
6. Open a pull request using the template.

## Expectations

- Keep local mode working without credentials or network access.
- Do not commit `.env`, tokens, customer conversations, or private business data.
- Do not claim an integration works unless it is implemented and tested.
- Keep customer-facing text simple and respectful.
- Prefer small, reviewable changes over broad rewrites.
- Update documentation when behavior or configuration changes.

## Commit and PR guidance

Use honest messages such as `feat: add booking adapter interface` or `test: expand Hinglish timing cases`. A pull request should explain the problem, approach, tests, privacy impact, and remaining limitations.

By contributing, you agree that your contribution is licensed under the repository's MIT License.
