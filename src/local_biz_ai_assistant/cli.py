"""Command-line interface for local use and validation."""

import argparse
import json

import uvicorn

from local_biz_ai_assistant.api import create_app
from local_biz_ai_assistant.config import load_business_profile, load_settings
from local_biz_ai_assistant.errors import LocalBizAssistantError
from local_biz_ai_assistant.service import create_service


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="local-biz-ai", description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    ask = subparsers.add_parser("ask", help="Ask one customer question.")
    ask.add_argument("query")
    ask.add_argument("--language", choices=["auto", "english", "hinglish"], default="auto")
    ask.add_argument("--json", action="store_true", help="Print structured JSON output.")

    serve = subparsers.add_parser("serve", help="Start the local HTTP API.")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8000)

    subparsers.add_parser("validate-config", help="Validate environment and business profile.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        settings = load_settings()
        if args.command == "validate-config":
            profile = load_business_profile(settings.profile_path)
            print(f"Configuration is valid for '{profile.name}' in {settings.provider} mode.")
            return 0
        service = create_service(settings=settings)
        if args.command == "ask":
            response = service.answer(args.query, args.language)
            print(response.model_dump_json(indent=2) if args.json else response.answer)
            return 0
        application = create_app(service)
        uvicorn.run(application, host=args.host, port=args.port, log_config=None)
        return 0
    except LocalBizAssistantError as exc:
        print(json.dumps({"error": str(exc)}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
