---
name: full-stack-generator
description: |
  Generate production-ready full-stack web applications with frontend, backend, PostgreSQL/MySQL/MongoDB, authentication, testing, CI/CD, deployment, boilerplate, configuration, and infrastructure.
  Practices: clean architecture, TDD setup, security, performance, accessibility, internationalization, consistency, customization, generated documentation.
  TRIGGERS: full-stack, scaffold, generate app, create project, bootstrap, new app, starter, boilerplate, project generator, web app, application scaffold
user-invocable: true
---

# Full-Stack Generator

Generate complete applications in six phases while preserving stack-specific configuration and operational safeguards.

Clean architecture retains separation of concerns, dependency inversion, single responsibility, open/closed, and interface segregation principles while automating setup that otherwise takes days.

The base command launches a wizard for project metadata, frontend, backend, database, authentication, features, and deployment. `init` defaults to Next.js+TypeScript, NestJS, PostgreSQL+Prisma, JWT, Jest, and Playwright; `config` opens `.fullstack.yaml`.

## Supported stacks and tools

### Frontend

- React 18.2: hooks; Redux Toolkit/Zustand/React Context; React Router v6 lazy routes; Tailwind/Styled Components/CSS Modules; React Hook Form+Zod; TanStack Query; Jest/React Testing Library/Cypress.
- Vue 3.4: Composition API; Pinia; Vue Router 4; Tailwind/Vuetify/CSS Modules; VeeValidate+Zod; Vue Query; Vitest/Vue Testing Library/Cypress.
- Next.js 14 (configuration 14.1): App Router, React Server Components, API handlers, Tailwind dark mode, NextAuth.js, Prisma, Jest, Playwright.
- Nuxt 3.9: Nitro, auto-imports, server routes, Tailwind/UnoCSS, Nuxt Auth, Vitest, Playwright.
- Angular 17.1: standalone components, Signals, lazy Angular Router, NgRx/Akita, Reactive Forms, HttpClient interceptors, Tailwind/Angular Material, Jasmine/Karma/Protractor.
- SvelteKit 2.0: SSR, file routing, Tailwind/vanilla CSS, form actions, server API routes, Vitest, Playwright.

### Backend

- Express 4.18/TypeScript: clean/MVC/hexagonal; Zod/Joi; JWT/OAuth2/session; TypeORM/Prisma/Mongoose; PostgreSQL/MySQL/MongoDB; Redis; Winston/Pino; Swagger/OpenAPI; express-rate-limit; Helmet/CORS/CSP; Jest/Supertest.
- Fastify 4.25/TypeScript: JSON Schema/TypeBox, plugins, @fastify/jwt/oauth2/redis/swagger, Prisma/TypeORM, PostgreSQL/MySQL, Pino, Tap/Jest.
- NestJS 10.3/TypeScript: DI modules, class-validator/class-transformer, Passport, TypeORM/Prisma/Mongoose, PostgreSQL/MySQL/MongoDB, Redis, Bull, Socket.io, Apollo, gRPC/RabbitMQ/Kafka, Swagger, Jest.
- FastAPI 0.109/Python 3.11: async, Pydantic, OAuth2-JWT, SQLAlchemy/Tortoise, PostgreSQL/MySQL, Redis/aioredis, Celery, Swagger/ReDoc, pytest/pytest-asyncio.
- Django 5.0/Python 3.11: Django REST Framework, JWT/OAuth2/session, Django ORM migrations, PostgreSQL/MySQL, django-redis, Celery, admin, drf-spectacular, pytest-django.
- Gin 1.9/Go 1.21: clean interfaces, go-playground/validator, JWT, GORM, PostgreSQL/MySQL, go-redis, Zap, swaggo, testify/gomock.
- Fiber 2.52/Go 1.21: clean architecture, validator, JWT, GORM/Ent, PostgreSQL/MySQL, go-redis, Zerolog, Swagger, testify.
- Actix-web 4.4/Rust 1.75: Tokio, validator, actix-web-httpauth, Diesel/SeaORM, PostgreSQL/MySQL, redis-rs, tracing, utoipa, actix-rt.

Supported database choices are exactly PostgreSQL, MySQL, and MongoDB, subject to each framework table above.

## Commands

### Primary and frontend

~~~text
/full-stack-generator
/full-stack-generator init my-awesome-app
/full-stack-generator config

/full-stack-generator frontend react
/full-stack-generator frontend vue
/full-stack-generator frontend nextjs
/full-stack-generator frontend nuxt
/full-stack-generator frontend angular
/full-stack-generator frontend sveltekit

/full-stack-generator frontend add-component Button
/full-stack-generator frontend add-component UserProfile --with-tests
/full-stack-generator frontend add-component DataTable --with-stories
/full-stack-generator frontend add-page Dashboard
/full-stack-generator frontend add-page Settings --layout admin
~~~

Frontend options: --typescript/--no-typescript (enabled by default); --styling tailwind|css-modules|styled-components; --state redux|zustand|pinia|ngrx; --testing jest|vitest. Components also accept --path, --with-tests, --with-stories. Pages accept --layout, --protected, --with-api.

### Backend and database

~~~text
/full-stack-generator backend express
/full-stack-generator backend fastify
/full-stack-generator backend nestjs
/full-stack-generator backend fastapi
/full-stack-generator backend django
/full-stack-generator backend gin
/full-stack-generator backend fiber
/full-stack-generator backend actix

/full-stack-generator backend add-module users
/full-stack-generator backend add-module products --with-crud
/full-stack-generator backend add-module orders --with-events
/full-stack-generator backend add-endpoint /api/users
/full-stack-generator backend add-endpoint /api/products --methods GET,POST,PUT,DELETE

/full-stack-generator database init
/full-stack-generator database add-model User
/full-stack-generator database add-model Product --fields "name:string,price:decimal,stock:integer"
/full-stack-generator database migrate
/full-stack-generator database migrate --seed
/full-stack-generator database migrate --fresh
~~~

Backend options: --database postgresql|mysql|mongodb; --orm prisma|typeorm|sqlalchemy|gorm; --auth jwt|oauth2|session; --docker. Modules also accept --with-crud, --with-events, --with-queue. Endpoints accept --methods, --auth, --validation. Models accept --fields, --relations, --timestamps, --soft-delete. The --fresh migration drops all tables before rerunning migrations.

### Tests and DevOps

~~~text
/full-stack-generator test setup
/full-stack-generator test add unit UserService
/full-stack-generator test add integration AuthController
/full-stack-generator test add e2e login-flow

/full-stack-generator devops docker
/full-stack-generator devops ci github
/full-stack-generator devops ci gitlab
/full-stack-generator devops ci jenkins
/full-stack-generator devops ci circleci
/full-stack-generator devops deploy aws
/full-stack-generator devops deploy gcp
/full-stack-generator devops deploy azure
/full-stack-generator devops deploy vercel
/full-stack-generator devops deploy railway
/full-stack-generator devops deploy fly
~~~

Test additions accept --coverage and --watch. Docker generation creates per-service Dockerfile, docker-compose.yml, docker-compose.prod.yml, and .dockerignore. CI targets GitHub Actions, GitLab, Jenkins, or CircleCI.

## Configuration: .fullstack.yaml

The config command opens this file. Its compact reference preserves the source controls:

~~~yaml
project: { name: my-awesome-app, description: "A full-stack web application", version: 1.0.0, author: "Your Name", license: MIT }
frontend:
  framework: nextjs
  version: "14.1"
  typescript: true
  package_manager: pnpm
  ui: { styling: tailwind, component_library: shadcn, icons: lucide, fonts: [Inter, JetBrains Mono], dark_mode: true }
  state: { solution: zustand, persist: true, devtools: true }
  routing: { type: app-router, middleware: true, i18n: { enabled: true, locales: [en, zh-TW, ja], default: en } }
  forms: { library: react-hook-form, validation: zod }
  api: { client: tanstack-query, base_url: /api, retry: true, cache: true }
  testing:
    unit: { framework: jest, coverage: 80 }
    component: { framework: testing-library }
    e2e: { framework: playwright, browsers: [chromium, firefox, webkit] }
  build: { output: standalone, analyze: true, sourcemaps: false }
backend:
  framework: nestjs
  version: "10.3"
  typescript: true
  package_manager: pnpm
  architecture: { pattern: clean, modules: [users, auth, products, orders] }
  api: { type: rest, versioning: true, prefix: /api/v1, documentation: { enabled: true, path: /docs } }
  validation: { library: class-validator, transform: true, whitelist: true }
  authentication:
    strategy: jwt
    providers: [local, google, github]
    jwt: { access_token_ttl: 15m, refresh_token_ttl: 7d }
    oauth: { callback_url: /auth/callback }
  database:
    orm: prisma
    type: postgresql
    host: localhost
    port: 5432
    name: myapp
    ssl: false
    pool: { min: 2, max: 10 }
    migrations: { auto: true }
  caching: { enabled: true, store: redis, ttl: 3600, host: localhost, port: 6379 }
  queue: { enabled: true, driver: bull, redis: { host: localhost, port: 6379 }, queues: [emails, notifications, reports] }
  logging: { level: info, format: json, transports: [console, file], file: { path: logs/app.log, rotate: true, max_size: 10MB, max_files: 5 } }
  security:
    helmet: true
    cors: { enabled: true, origins: [http://localhost:3000, https://myapp.com] }
    rate_limit: { enabled: true, window: 15m, max_requests: 100 }
    csrf: true
  testing:
    unit: { framework: jest, coverage: 80 }
    integration: { framework: supertest }
    e2e: { framework: jest, database: test }
~~~

Models preserve User/Post/Product/Order/OrderItem/Category fields, relations, indexes, unique/optional/default values, role USER|ADMIN, order states PENDING|PROCESSING|SHIPPED|DELIVERED|CANCELLED, decimal(10,2), and refresh-token storage. Key defaults include false/true booleans and stock 0.

~~~yaml
devops:
  docker: { enabled: true, registry: ghcr.io, compose: { version: "3.8", services: [app, db, redis, nginx] } }
  ci:
    platform: github-actions
    branches: { main: [lint, test, build, deploy], develop: [lint, test, build], "feature/*": [lint, test] }
    environments:
      staging: { branch: develop, auto_deploy: true }
      production: { branch: main, auto_deploy: false, approval_required: true }
  deployment:
    target: aws
    region: us-east-1
    services:
      frontend: { type: cloudfront, origin: s3 }
      backend: { type: ecs, cluster: myapp-cluster, service: myapp-api }
      database: { type: rds, instance: db.t3.micro }
      cache: { type: elasticache, node: cache.t3.micro }
  monitoring:
    enabled: true
    apm: datadog
    logging: cloudwatch
    alerts:
      - { type: error_rate, threshold: 5%, channel: slack }
      - { type: latency, threshold: 500ms, channel: email }
environment:
  development: { NODE_ENV: development, DATABASE_URL: postgresql://localhost:5432/myapp_dev, REDIS_URL: redis://localhost:6379, JWT_SECRET: dev-secret-key }
  staging: { NODE_ENV: staging, DATABASE_URL: env, REDIS_URL: env, JWT_SECRET: env }
  production: { NODE_ENV: production, DATABASE_URL: env, REDIS_URL: env, JWT_SECRET: env }
~~~

Treat development values as placeholders; staging/production secrets must come from environment secret management.

## 12. Deployment, generation phases, and formats

1. Init: create root/frontend/backend/shared/docs/config directories, Git/.gitignore/initial commit, package/workspace files, .env.example, environment configs, secret management.
2. Frontend: install/configure framework, TypeScript/build tools, UI/theme, stores/devtools, router/guards, API client/hooks/interceptors, test utilities/examples.
3. Backend: install/configure framework, ORM/driver/models/migrations, auth middleware/endpoints/token management, controllers/services/repositories/DI, validation schemas/middleware, Swagger/OpenAPI UI/spec, tests.
4. Integration: generate API/shared types, validate contracts, connect URLs/proxy/CORS, token refresh and protected routes.
5. DevOps: multi-stage Docker, CI testing/deployment, optional Terraform IaC, cloud resources, monitoring.
6. Docs: README.md, CONTRIBUTING.md, API/auth/error reference, deployment guide, architecture/component/data-flow diagrams, code style/PR/testing guidance.

Generated formats include YAML, JSON, TypeScript/JavaScript, Prisma schema/migrations, Markdown, .env files, Dockerfile/docker-compose, OpenAPI, HTML docs, shell/deploy scripts, and optional Terraform. Frontend and backend trees separate app/components/hooks/stores/lib/types/tests from modules/common/config/database/tests; shared API types connect them.

## Security and correctness invariants

- Validate and whitelist requests; use Helmet, CORS, CSP, CSRF, and rate limiting. Never commit production secrets.
- Hash new/updated passwords with bcrypt cost 10; never return password fields. Users update only themselves unless Role.ADMIN; admin-only create/delete routes use guards.
- Login returns the same “Invalid credentials” response for missing users and bad passwords. Duplicate registration is 409; successful registration is 201; login is 200; invalid credentials are 401.
- Issue separate JWT access/refresh secrets with 15m/7d TTLs; store refresh tokens with expiry, reject missing/expired stored tokens as “Invalid refresh token,” rotate/delete the old token on refresh, delete matching tokens on logout, and convert exp seconds with ×1000.
- API types, CORS, auth refresh, protected routes, validation, Swagger/OpenAPI, dependency injection, clean separation, strict TypeScript, accessibility, i18n, and tests are generated—not optional prose.
- Reference CI uses Node 20, pnpm 8, PostgreSQL 15 on 5432, Redis 7 on 6379, health interval 10s, timeout 5s, retries 5; coverage target is 80%. Build retains `needs: [lint, test]`; deploy retains `needs: [build]` and `refs/heads/main`. Docker exposes port 3000 and Compose 3.8.
- UI example retains focus ring 2, ring offset 2, opacity 50, primary hover 90, and button heights 9/10/11; pagination defaults page 1/limit 10. These are example constants, not universal policy.

Build/container command details retain pnpm install --frozen-lockfile, Docker COPY --from=deps and COPY --from=builder stages, plus PostgreSQL health flags --health-cmd, --health-interval 10s, --health-timeout 5s, and --health-retries 5.

## 13. End-to-end examples

~~~bash
/full-stack-generator init my-saas-app \
  --frontend nextjs \
  --backend nestjs \
  --database postgresql \
  --auth jwt \
  --features subscription,teams,billing

/full-stack-generator init my-shop \
  --frontend nuxt \
  --backend fastapi \
  --database postgresql \
  --auth oauth2 \
  --features products,cart,checkout,payments

/full-stack-generator init my-blog \
  --frontend sveltekit \
  --backend express \
  --database mongodb \
  --auth session \
  --features posts,comments,tags
~~~

## 14. Troubleshooting

~~~bash
# Database
docker-compose ps
echo $DATABASE_URL
npx prisma db push

# JWT
echo $JWT_ACCESS_SECRET
echo $JWT_REFRESH_SECRET
node -e "console.log(require('crypto').randomBytes(64).toString('hex'))"

# Build (destructive cache cleanup; run only in the intended project)
rm -rf node_modules
pnpm install
rm -rf .next dist
pnpm build
~~~

Database errors: verify service and connection string. Auth errors: verify both JWT secrets and regenerate with 64 random bytes. Build errors: clear only the listed local caches, reinstall, and rebuild.

References: [Next.js](https://nextjs.org/docs), [NestJS](https://docs.nestjs.com), [Prisma](https://www.prisma.io/docs), [Tailwind CSS](https://tailwindcss.com/docs).
