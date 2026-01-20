---
name: api-tester
description: |
  API testing and validation for RESTful APIs and GraphQL endpoints. Test, debug, and validate APIs with HTTP requests, authentication, schema validation, and automated test suites.

  Protocols: REST APIs, GraphQL, WebSockets, gRPC (beta)

  HTTP Methods: GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS

  Authentication: API Key, Bearer Token, OAuth2 (client_credentials, authorization code flow), Basic Auth

  Request Bodies: JSON, XML, form-data, raw

  Response Validation: JSON Schema, custom validators

  Features: HTTP requests, response validation, environment management, collection management, automated test execution, performance metrics, mock server setup, chain requests, load testing, documentation generation

  Assertions: status, body, headers, time, length

  Performance Metrics: Total Time, DNS Lookup, TCP Connect, TLS Handshake, Time to First Byte, Content Download, Response Size
---

# API Tester Skill

API testing, validation, and debugging.

## Protocols

- **REST APIs**: All HTTP methods and RESTful conventions
- **GraphQL**: Query and mutation support with variables
- **WebSockets**: Connection testing and message exchange
- **gRPC**: Protocol buffer-based service testing (beta)

## Authentication

### API Key
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

### Basic Auth
```json
{
  "auth": {
    "type": "basic",
    "username": "user",
    "password": "pass"
  }
}
```

## Features

### HTTP Requests

HTTP Methods: GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS

Request Bodies: JSON, XML, form-data, raw

#### GET Request
```
GET https://api.example.com/users/123
Headers:
  Accept: application/json
  X-API-Key: your-key
```

#### POST Request
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

Validate against JSON Schema or custom validators:

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

### Collection Management

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

## Commands

```bash
# GET request
/api-tester get https://api.example.com/users

# POST request with JSON body
/api-tester post https://api.example.com/users --body '{"name":"John"}'

# Run test collection
/api-tester run collection.yaml --env staging

# Validate response against schema
/api-tester validate response.json --schema user.schema.json

# Test with authentication
/api-tester get https://api.example.com/protected --auth bearer:token123

# Chain requests (use output from one as input to another)
/api-tester chain create-and-get.yaml

# Load testing
/api-tester load https://api.example.com/users --requests 100 --concurrency 10

# Generate API documentation from tests
/api-tester docs collection.yaml --output api-docs.md
```

## Assertions

| Assertion | Description | Example |
|-----------|-------------|---------|
| `status` | HTTP status code | `status == 200` |
| `body` | Response body content | `body.name == "John"` |
| `headers` | Response headers | `headers.content-type contains "json"` |
| `time` | Response time | `time < 500` (milliseconds) |
| `length` | Array/string length | `body.items.length >= 10` |

## Performance Metrics

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

- **Connection Errors**: Clear messages when target API is unreachable
- **Timeout Errors**: Configurable timeouts with informative messages
- **SSL/TLS Errors**: Options to skip certificate validation for testing
- **Authentication Errors**: Detailed feedback on auth failures

## Best Practices

1. **Environment Variables**: Never hardcode sensitive values like API keys
2. **Version Control**: Keep test collections in version control
3. **Edge Cases**: Test error conditions, not just happy paths
4. **Documentation**: Use clear test names and descriptions
5. **Response Times**: Set reasonable time assertions to catch performance regressions

## Limitations

- WebSocket support limited to basic connection testing
- OAuth 2.0 authorization code flow requires manual browser interaction
- File upload testing has 10MB limit per file
- GraphQL subscriptions not supported
