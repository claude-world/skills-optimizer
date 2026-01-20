---
name: api-tester
description: |
  This skill provides comprehensive API testing and validation capabilities that enable Claude
  to help users test, debug, and validate RESTful APIs and GraphQL endpoints. The skill is
  designed to assist developers in ensuring their APIs work correctly, handle edge cases
  properly, and return expected responses.

  The skill supports a wide variety of HTTP methods and authentication mechanisms, making it
  suitable for testing both simple public APIs and complex authenticated enterprise endpoints.
  Users can send requests, inspect responses, validate schemas, and run automated test suites.

  Key capabilities include:
  - Sending HTTP requests (GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS)
  - Multiple authentication methods (API Key, Bearer Token, OAuth2, Basic Auth)
  - Request body support (JSON, XML, form-data, raw)
  - Response validation against JSON Schema or custom validators
  - Environment variable management for different deployment stages
  - Collection management for organizing related API tests
  - Automated test execution with assertions
  - Performance metrics and timing analysis
  - Mock server setup for testing client applications

  Use this skill when you need to help users with API development tasks such as debugging
  endpoint issues, validating API responses, creating test suites, or understanding how
  an API works. The skill is particularly valuable during development and QA phases of
  API projects.
---

# API Tester Skill

A comprehensive skill for testing, validating, and debugging APIs.

## Overview

The API Tester skill helps developers and QA engineers test their APIs efficiently. It provides tools for making HTTP requests, validating responses, and managing test collections.

## Supported Protocols

This skill supports the following protocols and API styles:

- **REST APIs**: Full support for all HTTP methods and RESTful conventions
- **GraphQL**: Query and mutation support with variable handling
- **WebSockets**: Basic connection testing and message exchange
- **gRPC**: Protocol buffer-based service testing (beta)

## Authentication Methods

The skill supports various authentication mechanisms commonly used in APIs:

### API Key Authentication

```json
{
  "auth": {
    "type": "api-key",
    "key": "X-API-Key",
    "value": "your-api-key-here",
    "location": "header"
  }
}
```

### Bearer Token

```json
{
  "auth": {
    "type": "bearer",
    "token": "your-jwt-token-here"
  }
}
```

### OAuth 2.0

```json
{
  "auth": {
    "type": "oauth2",
    "grant_type": "client_credentials",
    "client_id": "your-client-id",
    "client_secret": "your-client-secret",
    "token_url": "https://auth.example.com/token"
  }
}
```

### Basic Authentication

```json
{
  "auth": {
    "type": "basic",
    "username": "user",
    "password": "pass"
  }
}
```

## Core Features

### Making Requests

The skill can send any type of HTTP request:

#### GET Request Example
```
GET https://api.example.com/users/123
Headers:
  Accept: application/json
  X-API-Key: your-key
```

#### POST Request Example
```
POST https://api.example.com/users
Headers:
  Content-Type: application/json
Body:
  {
    "name": "John Doe",
    "email": "john@example.com"
  }
```

### Response Validation

Validate API responses against expected schemas:

```yaml
validation:
  status: 200
  headers:
    content-type: application/json
  body:
    type: object
    required:
      - id
      - name
    properties:
      id:
        type: integer
      name:
        type: string
```

### Environment Management

Manage different environments for your API tests:

```yaml
environments:
  development:
    base_url: http://localhost:3000
    api_key: dev-key-123

  staging:
    base_url: https://staging.api.example.com
    api_key: staging-key-456

  production:
    base_url: https://api.example.com
    api_key: prod-key-789
```

### Test Collections

Organize related tests into collections:

```yaml
collection: User API Tests
tests:
  - name: List all users
    request:
      method: GET
      url: /users
    assertions:
      - status == 200
      - body.length > 0

  - name: Get single user
    request:
      method: GET
      url: /users/{{user_id}}
    assertions:
      - status == 200
      - body.id == user_id

  - name: Create user
    request:
      method: POST
      url: /users
      body:
        name: Test User
        email: test@example.com
    assertions:
      - status == 201
      - body.id exists
```

## Usage Commands

### Basic Commands

```bash
# Send a simple GET request
/api-tester get https://api.example.com/users

# Send POST request with JSON body
/api-tester post https://api.example.com/users --body '{"name":"John"}'

# Run a test collection
/api-tester run collection.yaml --env staging

# Validate response against schema
/api-tester validate response.json --schema user.schema.json
```

### Advanced Usage

```bash
# Test with authentication
/api-tester get https://api.example.com/protected --auth bearer:token123

# Chain requests (use output from one as input to another)
/api-tester chain create-and-get.yaml

# Performance testing
/api-tester load https://api.example.com/users --requests 100 --concurrency 10

# Generate API documentation from tests
/api-tester docs collection.yaml --output api-docs.md
```

## Assertions

The skill supports various assertion types for validating responses:

| Assertion | Description | Example |
|-----------|-------------|---------|
| `status` | HTTP status code | `status == 200` |
| `body` | Response body content | `body.name == "John"` |
| `headers` | Response headers | `headers.content-type contains "json"` |
| `time` | Response time | `time < 500` (milliseconds) |
| `length` | Array/string length | `body.items.length >= 10` |

## Performance Metrics

When running tests, the skill provides detailed performance metrics:

```
Response Metrics:
  Total Time: 245ms
  DNS Lookup: 12ms
  TCP Connect: 23ms
  TLS Handshake: 89ms
  Time to First Byte: 156ms
  Content Download: 34ms
  Response Size: 1.2KB
```

## Mock Server

Set up a mock server for testing client applications:

```yaml
mock:
  port: 8080
  routes:
    - method: GET
      path: /users
      response:
        status: 200
        body:
          - id: 1
            name: Mock User

    - method: POST
      path: /users
      response:
        status: 201
        body:
          id: "{{random.uuid}}"
          created: true
```

## Error Handling

The skill handles common API testing errors gracefully:

- **Connection Errors**: Clear messages when the target API is unreachable
- **Timeout Errors**: Configurable timeouts with informative messages
- **SSL/TLS Errors**: Options to skip certificate validation for testing
- **Authentication Errors**: Detailed feedback on auth failures

## Best Practices

1. **Use Environment Variables**: Never hardcode sensitive values like API keys
2. **Version Your Collections**: Keep test collections in version control
3. **Test Edge Cases**: Include tests for error conditions, not just happy paths
4. **Document Expected Behavior**: Use clear test names and descriptions
5. **Monitor Response Times**: Set reasonable time assertions to catch performance regressions

## Limitations

- WebSocket support is currently limited to basic connection testing
- OAuth 2.0 authorization code flow requires manual browser interaction
- File upload testing has a 10MB limit per file
- GraphQL subscriptions are not yet supported

## See Also

- [Request Examples](examples/requests.md)
- [Schema Validation Guide](guides/schema-validation.md)
- [CI/CD Integration](guides/ci-integration.md)
