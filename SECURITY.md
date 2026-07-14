# Security Policy

## Supported versions

Security fixes are maintained for the latest `0.1.x` release and the latest commit on `main`. Earlier template commits are not supported. The project is alpha software and is not production-ready.

## Report a vulnerability

Do not open a public issue for a vulnerability that could expose credentials, customer data, or a deployed service. Prefer GitHub's private vulnerability-reporting or Security Advisory flow if it is available for this repository. Otherwise, contact the maintainer privately through GitHub without including secrets in the first message.

Include:

- affected version or commit;
- affected file or endpoint;
- safe reproduction steps;
- possible impact;
- suggested mitigation, if known.

Never send real API keys, production customer data, passwords, cookies, or access tokens. Use placeholders and fictional test data.

## Current security boundaries

- Local mode makes no external AI-provider request.
- Remote mode sends the customer query and configured business profile to the selected provider.
- Provider API keys are read from environment variables and are not intentionally logged.
- Base URLs require HTTPS except for localhost and reject embedded credentials, query strings, and fragments.
- Customer query length is capped at 1,000 characters.
- The default logs omit query text.

## Not yet implemented

The API has no authentication, authorization, rate limiting, abuse detection, persistent storage protection, tenant isolation, or deployment hardening. Do not expose this MVP directly to the public internet. Put authentication, TLS, rate limiting, request-size limits, and monitoring in front of any deployment.

## Response process

The maintainer will validate the report, assess impact, prepare a focused fix and regression test, and coordinate disclosure when practical. No bounty or guaranteed response time is currently offered.
