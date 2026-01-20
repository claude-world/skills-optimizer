---
name: full-stack-generator
description: |
  Full-stack app generator. Scaffolds frontend, backend, database, auth, testing, CI/CD, deployment.
  TRIGGERS: full-stack, scaffold, generate app, create project, bootstrap, new app, starter, boilerplate, project generator, web app, application scaffold
user-invocable: true
---

# Full-Stack Generator

Generate complete web apps with frontend, backend, database, auth, testing, CI/CD.

## Supported Stacks

### Frontend
| Framework | State | Styling | Testing |
|-----------|-------|---------|---------|
| React 18 | Redux Toolkit, Zustand, Context | Tailwind, Styled Components, CSS Modules | Jest, RTL, Cypress |
| Vue 3 | Pinia | Tailwind, Vuetify, CSS Modules | Vitest, VTL, Cypress |
| Next.js 14 | Zustand, Context | Tailwind | Jest, Playwright |
| Nuxt 3 | Pinia | Tailwind, UnoCSS | Vitest, Playwright |
| Angular 17 | NgRx, Akita | Tailwind, Angular Material | Jasmine, Protractor |
| SvelteKit 2 | Built-in | Tailwind | Vitest, Playwright |

### Backend
| Framework | Language | ORM | Auth |
|-----------|----------|-----|------|
| Express 4 | Node/TS | TypeORM, Prisma, Mongoose | JWT, OAuth2, Session |
| Fastify 4 | Node/TS | Prisma, TypeORM | JWT, OAuth2 |
| NestJS 10 | Node/TS | TypeORM, Prisma, Mongoose | Passport |
| FastAPI | Python 3.11 | SQLAlchemy, Tortoise | OAuth2-JWT |
| Django 5 | Python 3.11 | Django ORM | JWT, OAuth2, Session |
| Gin 1.9 | Go 1.21 | GORM | JWT |
| Fiber 2 | Go 1.21 | GORM, Ent | JWT |
| Actix 4 | Rust 1.75 | Diesel, SeaORM | JWT |

### Database
PostgreSQL, MySQL, MongoDB, SQLite, SQL Server, Oracle, Cassandra

## Commands

```bash
# Interactive wizard
/full-stack-generator

# Quick init with defaults (Next.js + NestJS + PostgreSQL)
/full-stack-generator init <name>

# Frontend only
/full-stack-generator frontend <react|vue|nextjs|nuxt|angular|sveltekit>
  --typescript --styling <tailwind|css-modules> --state <redux|zustand|pinia>

# Backend only
/full-stack-generator backend <express|fastify|nestjs|fastapi|django|gin|fiber|actix>
  --database <postgresql|mysql|mongodb> --orm <prisma|typeorm> --auth <jwt|oauth2>

# Add components
/full-stack-generator frontend add-component <Name> [--with-tests] [--with-stories]
/full-stack-generator frontend add-page <Name> [--protected] [--layout <name>]
/full-stack-generator backend add-module <name> [--with-crud] [--with-events]
/full-stack-generator backend add-endpoint <path> [--methods GET,POST] [--auth]

# Database
/full-stack-generator database init
/full-stack-generator database add-model <Name> --fields "name:string,price:decimal"
/full-stack-generator database migrate [--seed] [--fresh]

# Testing
/full-stack-generator test setup
/full-stack-generator test add <unit|integration|e2e> <Name>

# DevOps
/full-stack-generator devops docker
/full-stack-generator devops ci <github|gitlab|jenkins|circleci>
/full-stack-generator devops deploy <aws|gcp|azure|vercel|railway|fly>
```

## Generation Phases

| Phase | Action |
|-------|--------|
| 1. Init | Create dirs, git, package.json, .env |
| 2. Frontend | Framework, components, state, routing, API client, tests |
| 3. Backend | Framework, modules, auth, validation, docs, tests |
| 4. Integration | API types, CORS, auth flow |
| 5. DevOps | Dockerfiles, CI/CD, deploy scripts |
| 6. Docs | README, API docs, architecture |

## Config (.fullstack.yaml)

```yaml
project:
  name: my-app

frontend:
  framework: nextjs
  typescript: true
  styling: tailwind
  state: zustand
  api: tanstack-query
  testing: { unit: jest, e2e: playwright }

backend:
  framework: nestjs
  typescript: true
  database: { orm: prisma, type: postgresql }
  auth: { strategy: jwt, providers: [local, google, github] }
  caching: redis
  queue: bull
  logging: { level: info, format: json }
  security: { helmet: true, cors: true, rate_limit: true }

models:
  User: { fields: [id:uuid, email:string, password:string, role:enum] }
  Product: { fields: [id:uuid, name:string, price:decimal, stock:int] }
  Order: { fields: [id:uuid, userId:uuid, status:enum, total:decimal] }

devops:
  docker: true
  ci: github-actions
  deploy: { target: aws, region: us-east-1 }
```

## Directory Structure

```
project/
├── frontend/
│   ├── src/
│   │   ├── app/           # Pages/routes
│   │   ├── components/    # UI, forms, layouts, features
│   │   ├── hooks/         # Custom hooks
│   │   ├── stores/        # State management
│   │   ├── lib/           # Utils, API client
│   │   └── types/         # TypeScript types
│   └── tests/
├── backend/
│   ├── src/
│   │   ├── modules/       # auth, users, products, orders
│   │   ├── common/        # decorators, guards, filters
│   │   ├── config/        # app, database, jwt config
│   │   └── database/      # prisma schema, migrations
│   └── test/
├── docker-compose.yml
└── .github/workflows/
```

## Features

- Clean architecture (separation of concerns, DI)
- TypeScript strict mode
- JWT + OAuth2 (Google, GitHub)
- Prisma migrations + seeding
- Redis caching + Bull queues
- Swagger/OpenAPI docs
- Jest + Playwright testing
- Docker multi-stage builds
- GitHub Actions CI/CD
- AWS/GCP/Vercel deployment

## Troubleshooting

| Issue | Solution |
|-------|----------|
| DB connection failed | Check DATABASE_URL, run `docker-compose ps` |
| Auth not working | Verify JWT_SECRET, regenerate with `crypto.randomBytes(64)` |
| Build failing | `rm -rf node_modules .next dist && pnpm install && pnpm build` |
