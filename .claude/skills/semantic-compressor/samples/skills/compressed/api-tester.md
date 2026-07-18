---
name: api-tester
description: |
  Test, debug, and validate RESTful APIs, GraphQL endpoints, WebSockets, and gRPC services using requests, authentication, schema validation, collections, assertions, performance metrics, and mock servers.
  TRIGGERS: API testing, API validation, test API, debug API, endpoint issue, validate response, create API test suite, understand API behavior, API development, API QA, RESTful API, GraphQL
---

# API Tester

## Coverage

- Protocols: REST (GET/POST/PUT/DELETE/PATCH/HEAD/OPTIONS), GraphQL queries/mutations with variables, WebSocket connections/messages, gRPC/protocol buffers (beta).
- Authentication: API key (`X-API-Key`, header), bearer/JWT, OAuth 2.0 `client_credentials` or authorization-code flow, Basic username/password.
- Bodies/formats: JSON, XML, form-data, raw; JSON Schema/custom response validators; YAML environments, collections, and mock definitions; Markdown documentation output.
- Features: request/response inspection, development/staging/production variables, reusable collections, chained requests, automated assertions, load/timing analysis, documentation generation, mock routes.

## Commands

```text
/api-tester get https://api.example.com/users
/api-tester post https://api.example.com/users --body '{"name":"John"}'
/api-tester run collection.yaml --env staging
/api-tester validate response.json --schema user.schema.json
/api-tester get https://api.example.com/protected --auth bearer:token123
/api-tester chain create-and-get.yaml
/api-tester load https://api.example.com/users --requests 100 --concurrency 10
/api-tester docs collection.yaml --output api-docs.md
```

Direct request examples use `GET https://api.example.com/users/123` with `Accept: application/json`/`X-API-Key`, and JSON `POST https://api.example.com/users` with `Content-Type: application/json` plus name/email.

The canonical response schema requires status `200`, JSON content type, and an object body with required integer `id` and string `name` properties.

## Validation and reference values

- Assertions: `status == 200`, `body.name == "John"`, `headers.content-type contains "json"`, `time < 500` milliseconds, `body.items.length >= 10`; collection examples also require `body.length > 0`, create status `201`, and an existing body ID.
- Timing output retains Total `245ms`, DNS `12ms`, TCP `23ms`, TLS `89ms`, TTFB `156ms`, download `34ms`, response size `1.2KB`.
- Environment examples use `localhost:3000`, staging/production HTTPS URLs, and placeholder keys `dev-key-123`, `staging-key-456`, `prod-key-789`—never real secrets.
- Mock server example listens on port `8080`; GET `/users` returns status `200` with ID `1`/name `Mock User`; POST returns `201`, `created: true`, and `{{random.uuid}}`.

## Safety and limits

1. Use environment variables; never hardcode API keys or other sensitive values.
2. Keep test collections in version control.
3. Test failures and edge cases, not only happy paths.
4. Document expected behavior with clear test names/descriptions.
5. Set reasonable response-time assertions to detect regressions.
- Report connection, configurable-timeout, authentication, and SSL/TLS errors clearly. Certificate validation may be skipped only for testing.
- WebSockets support basic connection testing only; OAuth 2.0 authorization code requires manual browser interaction; uploads are limited to `10MB` per file; GraphQL subscriptions are unsupported.

References: request examples `examples/requests.md`, schema validation `guides/schema-validation.md`, CI/CD integration `guides/ci-integration.md`.
