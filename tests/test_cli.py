from local_biz_ai_assistant.cli import main


def test_cli_ask_in_local_mode(monkeypatch, capsys) -> None:  # type: ignore[no-untyped-def]
    monkeypatch.delenv("LOCAL_BIZ_PROVIDER", raising=False)
    exit_code = main(["ask", "What are your hours?"])
    output = capsys.readouterr().out
    assert exit_code == 0
    assert "Monday-Saturday" in output


def test_cli_validate_config(monkeypatch, capsys) -> None:  # type: ignore[no-untyped-def]
    monkeypatch.delenv("LOCAL_BIZ_PROVIDER", raising=False)
    exit_code = main(["validate-config"])
    assert exit_code == 0
    assert "Configuration is valid" in capsys.readouterr().out
