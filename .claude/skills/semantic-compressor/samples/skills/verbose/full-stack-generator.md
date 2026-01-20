---
name: full-stack-generator
description: |
  A comprehensive full-stack application generator that scaffolds complete web applications with frontend, backend, database, authentication, testing, CI/CD, and deployment configurations. This skill provides an end-to-end solution for creating production-ready applications following best practices and modern development patterns.

  This skill is designed to help developers quickly bootstrap new projects with all the necessary boilerplate code, configuration files, and infrastructure setup. It supports multiple technology stacks and can be customized to fit specific project requirements.

  The generator follows industry best practices including:
  - Clean architecture principles
  - Test-driven development setup
  - Security best practices
  - Performance optimization
  - Accessibility compliance
  - Internationalization support

  TRIGGERS: full-stack, scaffold, generate app, create project, bootstrap, new app, starter, boilerplate, project generator, web app, application scaffold
user-invocable: true
---

# Full-Stack Application Generator

A comprehensive skill for generating complete full-stack web applications with all necessary configurations, boilerplate code, and infrastructure setup. This generator supports multiple technology stacks and follows modern development best practices.

## Table of Contents

1. [Overview](#overview)
2. [Supported Technology Stacks](#supported-technology-stacks)
3. [Commands](#commands)
4. [Configuration Options](#configuration-options)
5. [Generation Phases](#generation-phases)
6. [Frontend Generation](#frontend-generation)
7. [Backend Generation](#backend-generation)
8. [Database Setup](#database-setup)
9. [Authentication](#authentication)
10. [Testing Setup](#testing-setup)
11. [CI/CD Configuration](#cicd-configuration)
12. [Deployment](#deployment)
13. [Examples](#examples)
14. [Troubleshooting](#troubleshooting)

---

## Overview

The Full-Stack Application Generator is designed to eliminate the tedious process of setting up new projects from scratch. Instead of spending hours configuring build tools, setting up testing frameworks, and creating boilerplate code, developers can use this skill to generate a complete, production-ready application in minutes.

### Key Benefits

The generator provides numerous benefits to development teams:

1. **Time Savings**: Reduce project setup time from days to minutes by automating the creation of all necessary files and configurations.

2. **Consistency**: Ensure all projects follow the same structure and coding standards, making it easier for team members to switch between projects.

3. **Best Practices**: Built-in best practices for security, performance, and maintainability that would otherwise require extensive research and implementation.

4. **Customization**: Flexible configuration options allow teams to adapt the generated code to their specific needs and preferences.

5. **Documentation**: Automatically generated documentation helps new team members understand the project structure and conventions.

### Architecture Philosophy

The generated applications follow clean architecture principles:

- **Separation of Concerns**: Each layer of the application has a single responsibility and is isolated from other layers.

- **Dependency Inversion**: High-level modules do not depend on low-level modules; both depend on abstractions.

- **Single Responsibility**: Each module, class, or function has one reason to change.

- **Open/Closed Principle**: Modules are open for extension but closed for modification.

- **Interface Segregation**: Clients should not be forced to depend on interfaces they do not use.

---

## Supported Technology Stacks

### Frontend Frameworks

The generator supports the following frontend frameworks and libraries:

#### React

React is a JavaScript library for building user interfaces. The generator creates React applications with the following features:

- **Component Structure**: Functional components with hooks
- **State Management**: Redux Toolkit, Zustand, or React Context
- **Routing**: React Router v6 with lazy loading
- **Styling**: Tailwind CSS, Styled Components, or CSS Modules
- **Form Handling**: React Hook Form with Zod validation
- **API Integration**: TanStack Query (React Query)
- **Testing**: Jest, React Testing Library, Cypress

Configuration options for React:

```yaml
frontend:
  framework: react
  version: "18.2"
  typescript: true
  state_management: redux-toolkit | zustand | context
  styling: tailwind | styled-components | css-modules
  routing: react-router
  forms: react-hook-form
  validation: zod
  api_client: tanstack-query
  testing:
    unit: jest
    component: react-testing-library
    e2e: cypress
```

#### Vue.js

Vue.js is a progressive JavaScript framework for building user interfaces. The generator creates Vue applications with:

- **Composition API**: Modern Vue 3 composition API patterns
- **State Management**: Pinia
- **Routing**: Vue Router 4
- **Styling**: Tailwind CSS, Vuetify, or CSS Modules
- **Form Handling**: VeeValidate with Zod
- **API Integration**: Vue Query
- **Testing**: Vitest, Vue Testing Library, Cypress

Configuration options for Vue:

```yaml
frontend:
  framework: vue
  version: "3.4"
  typescript: true
  state_management: pinia
  styling: tailwind | vuetify | css-modules
  routing: vue-router
  forms: vee-validate
  validation: zod
  api_client: vue-query
  testing:
    unit: vitest
    component: vue-testing-library
    e2e: cypress
```

#### Next.js

Next.js is a React framework for production-grade applications. The generator creates Next.js applications with:

- **App Router**: Next.js 14 App Router architecture
- **Server Components**: React Server Components support
- **API Routes**: Built-in API route handlers
- **Styling**: Tailwind CSS with dark mode support
- **Authentication**: NextAuth.js integration
- **Database**: Prisma ORM integration
- **Testing**: Jest, Playwright

Configuration options for Next.js:

```yaml
frontend:
  framework: nextjs
  version: "14.1"
  typescript: true
  app_router: true
  server_components: true
  styling: tailwind
  authentication: next-auth
  database: prisma
  testing:
    unit: jest
    e2e: playwright
```

#### Nuxt.js

Nuxt.js is a Vue framework for building modern web applications. The generator creates Nuxt applications with:

- **Nuxt 3**: Latest Nuxt 3 with Nitro server
- **Auto-imports**: Automatic component and composable imports
- **Server Routes**: Built-in API server routes
- **Styling**: Tailwind CSS, UnoCSS
- **Authentication**: Nuxt Auth module
- **Testing**: Vitest, Playwright

Configuration options for Nuxt:

```yaml
frontend:
  framework: nuxt
  version: "3.9"
  typescript: true
  styling: tailwind | unocss
  authentication: nuxt-auth
  testing:
    unit: vitest
    e2e: playwright
```

#### Angular

Angular is a platform for building mobile and desktop web applications. The generator creates Angular applications with:

- **Standalone Components**: Modern Angular standalone component architecture
- **Signals**: Angular Signals for reactivity
- **Routing**: Angular Router with lazy loading
- **State Management**: NgRx or Akita
- **Forms**: Reactive Forms with validation
- **HTTP**: HttpClient with interceptors
- **Testing**: Jasmine, Karma, Protractor

Configuration options for Angular:

```yaml
frontend:
  framework: angular
  version: "17.1"
  typescript: true
  standalone: true
  signals: true
  state_management: ngrx | akita
  styling: tailwind | angular-material
  forms: reactive
  testing:
    unit: jasmine
    e2e: protractor
```

#### Svelte/SvelteKit

Svelte is a radical new approach to building user interfaces. The generator creates SvelteKit applications with:

- **SvelteKit**: Full-featured framework with SSR
- **Routing**: File-based routing
- **Styling**: Tailwind CSS or vanilla CSS
- **Forms**: SvelteKit form actions
- **API**: Server-side API routes
- **Testing**: Vitest, Playwright

Configuration options for SvelteKit:

```yaml
frontend:
  framework: sveltekit
  version: "2.0"
  typescript: true
  styling: tailwind | css
  testing:
    unit: vitest
    e2e: playwright
```

### Backend Frameworks

The generator supports the following backend frameworks:

#### Node.js with Express

Express is a minimal and flexible Node.js web application framework. The generator creates Express applications with:

- **TypeScript**: Full TypeScript support with strict mode
- **Architecture**: Clean architecture with controllers, services, repositories
- **Validation**: Zod or Joi for request validation
- **Authentication**: JWT, OAuth2, session-based
- **Database**: TypeORM, Prisma, or Mongoose
- **Caching**: Redis integration
- **Logging**: Winston or Pino
- **API Documentation**: Swagger/OpenAPI
- **Rate Limiting**: express-rate-limit
- **Security**: Helmet, CORS, CSP headers
- **Testing**: Jest, Supertest

Configuration options for Express:

```yaml
backend:
  framework: express
  version: "4.18"
  typescript: true
  architecture: clean | mvc | hexagonal
  validation: zod | joi
  authentication: jwt | oauth2 | session
  database:
    orm: typeorm | prisma | mongoose
    type: postgresql | mysql | mongodb
  caching: redis
  logging: winston | pino
  documentation: swagger
  security:
    helmet: true
    cors: true
    rate_limit: true
  testing:
    unit: jest
    integration: supertest
```

#### Node.js with Fastify

Fastify is a fast and low overhead web framework for Node.js. The generator creates Fastify applications with:

- **TypeScript**: Full TypeScript support
- **Schema Validation**: JSON Schema validation
- **Plugins**: Modular plugin architecture
- **Authentication**: @fastify/jwt, @fastify/oauth2
- **Database**: Prisma, TypeORM
- **Caching**: @fastify/redis
- **Logging**: Built-in Pino logger
- **API Documentation**: @fastify/swagger
- **Testing**: Tap, Jest

Configuration options for Fastify:

```yaml
backend:
  framework: fastify
  version: "4.25"
  typescript: true
  validation: json-schema | typebox
  authentication: jwt | oauth2
  database:
    orm: prisma | typeorm
    type: postgresql | mysql
  caching: redis
  documentation: swagger
  testing:
    unit: tap | jest
```

#### NestJS

NestJS is a progressive Node.js framework for building efficient, reliable, and scalable server-side applications. The generator creates NestJS applications with:

- **TypeScript**: Native TypeScript support
- **Architecture**: Modular architecture with dependency injection
- **Validation**: class-validator, class-transformer
- **Authentication**: Passport.js integration
- **Database**: TypeORM, Prisma, Mongoose
- **Caching**: Cache Manager with Redis
- **Queue**: Bull queue integration
- **WebSockets**: Socket.io integration
- **GraphQL**: Apollo Server integration
- **Microservices**: gRPC, RabbitMQ, Kafka support
- **API Documentation**: Swagger with decorators
- **Testing**: Jest with mocking utilities

Configuration options for NestJS:

```yaml
backend:
  framework: nestjs
  version: "10.3"
  typescript: true
  validation: class-validator
  authentication: passport
  database:
    orm: typeorm | prisma | mongoose
    type: postgresql | mysql | mongodb
  caching: redis
  queue: bull
  websockets: socket.io
  graphql: apollo
  microservices: grpc | rabbitmq | kafka
  documentation: swagger
  testing:
    unit: jest
    e2e: jest
```

#### Python with FastAPI

FastAPI is a modern, fast web framework for building APIs with Python. The generator creates FastAPI applications with:

- **Type Hints**: Full Python type hints support
- **Async**: Async/await support throughout
- **Validation**: Pydantic models
- **Authentication**: OAuth2 with JWT
- **Database**: SQLAlchemy, Tortoise ORM
- **Caching**: Redis with aioredis
- **Background Tasks**: Celery integration
- **API Documentation**: Automatic Swagger/ReDoc
- **Testing**: pytest, pytest-asyncio

Configuration options for FastAPI:

```yaml
backend:
  framework: fastapi
  version: "0.109"
  python_version: "3.11"
  async: true
  validation: pydantic
  authentication: oauth2-jwt
  database:
    orm: sqlalchemy | tortoise
    type: postgresql | mysql
  caching: redis
  background_tasks: celery
  documentation: swagger
  testing:
    unit: pytest
    async: pytest-asyncio
```

#### Python with Django

Django is a high-level Python web framework that encourages rapid development. The generator creates Django applications with:

- **Django REST Framework**: For building APIs
- **Authentication**: JWT, OAuth2, session
- **Database**: Django ORM with migrations
- **Caching**: Redis with django-redis
- **Background Tasks**: Celery with Django
- **Admin**: Django admin customization
- **API Documentation**: drf-spectacular
- **Testing**: pytest-django

Configuration options for Django:

```yaml
backend:
  framework: django
  version: "5.0"
  python_version: "3.11"
  rest_framework: true
  authentication: jwt | oauth2 | session
  database:
    type: postgresql | mysql
  caching: redis
  background_tasks: celery
  admin: true
  documentation: drf-spectacular
  testing:
    unit: pytest-django
```

#### Go with Gin

Gin is a HTTP web framework written in Go. The generator creates Gin applications with:

- **Architecture**: Clean architecture with interfaces
- **Validation**: go-playground/validator
- **Authentication**: JWT middleware
- **Database**: GORM with migrations
- **Caching**: go-redis
- **Logging**: Zap logger
- **API Documentation**: Swagger with swaggo
- **Testing**: testify, gomock

Configuration options for Gin:

```yaml
backend:
  framework: gin
  version: "1.9"
  go_version: "1.21"
  validation: validator
  authentication: jwt
  database:
    orm: gorm
    type: postgresql | mysql
  caching: redis
  logging: zap
  documentation: swagger
  testing:
    unit: testify
    mocking: gomock
```

#### Go with Fiber

Fiber is an Express-inspired web framework built on top of Fasthttp. The generator creates Fiber applications with:

- **Architecture**: Clean architecture
- **Validation**: go-playground/validator
- **Authentication**: JWT middleware
- **Database**: GORM, Ent
- **Caching**: go-redis
- **Logging**: Zerolog
- **API Documentation**: Swagger
- **Testing**: testify

Configuration options for Fiber:

```yaml
backend:
  framework: fiber
  version: "2.52"
  go_version: "1.21"
  validation: validator
  authentication: jwt
  database:
    orm: gorm | ent
    type: postgresql | mysql
  caching: redis
  logging: zerolog
  documentation: swagger
  testing:
    unit: testify
```

#### Rust with Actix-web

Actix-web is a powerful, pragmatic, and extremely fast web framework for Rust. The generator creates Actix applications with:

- **Type Safety**: Full Rust type safety
- **Async**: Tokio runtime
- **Validation**: validator crate
- **Authentication**: actix-web-httpauth
- **Database**: Diesel, SeaORM
- **Caching**: redis-rs
- **Logging**: tracing
- **API Documentation**: utoipa
- **Testing**: actix-rt

Configuration options for Actix:

```yaml
backend:
  framework: actix
  version: "4.4"
  rust_version: "1.75"
  async_runtime: tokio
  validation: validator
  authentication: jwt
  database:
    orm: diesel | sea-orm
    type: postgresql | mysql
  caching: redis
  logging: tracing
  documentation: utoipa
  testing:
    unit: actix-rt
```

---

## Commands

The following commands are available for the full-stack generator:

### Primary Commands

#### `/full-stack-generator`

The main command to start the interactive project generation wizard.

```bash
/full-stack-generator
```

This command launches an interactive wizard that guides you through:
1. Project name and description
2. Frontend framework selection
3. Backend framework selection
4. Database selection
5. Authentication method
6. Additional features
7. Deployment target

#### `/full-stack-generator init <project-name>`

Quick initialization with default settings.

```bash
/full-stack-generator init my-awesome-app
```

Creates a new project with sensible defaults:
- Frontend: Next.js with TypeScript
- Backend: NestJS
- Database: PostgreSQL with Prisma
- Authentication: JWT
- Testing: Jest, Playwright

#### `/full-stack-generator config`

Opens the configuration file for advanced customization.

```bash
/full-stack-generator config
```

This opens the `.fullstack.yaml` configuration file where you can specify all options in detail.

### Frontend Commands

#### `/full-stack-generator frontend <framework>`

Generate only the frontend portion of the application.

```bash
/full-stack-generator frontend react
/full-stack-generator frontend vue
/full-stack-generator frontend nextjs
/full-stack-generator frontend nuxt
/full-stack-generator frontend angular
/full-stack-generator frontend sveltekit
```

Options:
- `--typescript` / `--no-typescript`: Enable/disable TypeScript (default: enabled)
- `--styling <option>`: Styling solution (tailwind, css-modules, styled-components)
- `--state <option>`: State management (redux, zustand, pinia, ngrx)
- `--testing <option>`: Testing framework (jest, vitest)

#### `/full-stack-generator frontend add-component <name>`

Add a new component to the frontend.

```bash
/full-stack-generator frontend add-component Button
/full-stack-generator frontend add-component UserProfile --with-tests
/full-stack-generator frontend add-component DataTable --with-stories
```

Options:
- `--with-tests`: Generate test files
- `--with-stories`: Generate Storybook stories
- `--path <path>`: Custom component path

#### `/full-stack-generator frontend add-page <name>`

Add a new page/route to the frontend.

```bash
/full-stack-generator frontend add-page Dashboard
/full-stack-generator frontend add-page Settings --layout admin
```

Options:
- `--layout <name>`: Use specific layout
- `--protected`: Add authentication guard
- `--with-api`: Generate corresponding API route

### Backend Commands

#### `/full-stack-generator backend <framework>`

Generate only the backend portion of the application.

```bash
/full-stack-generator backend express
/full-stack-generator backend fastify
/full-stack-generator backend nestjs
/full-stack-generator backend fastapi
/full-stack-generator backend django
/full-stack-generator backend gin
/full-stack-generator backend fiber
/full-stack-generator backend actix
```

Options:
- `--database <type>`: Database type (postgresql, mysql, mongodb)
- `--orm <option>`: ORM choice (prisma, typeorm, sqlalchemy, gorm)
- `--auth <option>`: Authentication method (jwt, oauth2, session)
- `--docker`: Include Docker configuration

#### `/full-stack-generator backend add-module <name>`

Add a new module/feature to the backend.

```bash
/full-stack-generator backend add-module users
/full-stack-generator backend add-module products --with-crud
/full-stack-generator backend add-module orders --with-events
```

Options:
- `--with-crud`: Generate CRUD operations
- `--with-events`: Generate event handlers
- `--with-queue`: Generate queue workers

#### `/full-stack-generator backend add-endpoint <path>`

Add a new API endpoint.

```bash
/full-stack-generator backend add-endpoint /api/users
/full-stack-generator backend add-endpoint /api/products --methods GET,POST,PUT,DELETE
```

Options:
- `--methods <list>`: HTTP methods to support
- `--auth`: Require authentication
- `--validation`: Add request validation

### Database Commands

#### `/full-stack-generator database init`

Initialize the database schema and migrations.

```bash
/full-stack-generator database init
```

#### `/full-stack-generator database add-model <name>`

Add a new database model/entity.

```bash
/full-stack-generator database add-model User
/full-stack-generator database add-model Product --fields "name:string,price:decimal,stock:integer"
```

Options:
- `--fields <spec>`: Field definitions
- `--relations <spec>`: Relationship definitions
- `--timestamps`: Add created_at/updated_at
- `--soft-delete`: Add soft delete support

#### `/full-stack-generator database migrate`

Run database migrations.

```bash
/full-stack-generator database migrate
/full-stack-generator database migrate --seed
```

Options:
- `--seed`: Run seeders after migration
- `--fresh`: Drop all tables and re-run migrations

### Testing Commands

#### `/full-stack-generator test setup`

Set up the testing infrastructure.

```bash
/full-stack-generator test setup
```

#### `/full-stack-generator test add <type> <name>`

Add a new test file.

```bash
/full-stack-generator test add unit UserService
/full-stack-generator test add integration AuthController
/full-stack-generator test add e2e login-flow
```

Options:
- `--coverage`: Add coverage configuration
- `--watch`: Set up watch mode

### DevOps Commands

#### `/full-stack-generator devops docker`

Generate Docker configuration.

```bash
/full-stack-generator devops docker
```

Generates:
- `Dockerfile` for each service
- `docker-compose.yml` for local development
- `docker-compose.prod.yml` for production
- `.dockerignore` files

#### `/full-stack-generator devops ci <platform>`

Generate CI/CD configuration.

```bash
/full-stack-generator devops ci github
/full-stack-generator devops ci gitlab
/full-stack-generator devops ci jenkins
/full-stack-generator devops ci circleci
```

#### `/full-stack-generator devops deploy <target>`

Generate deployment configuration.

```bash
/full-stack-generator devops deploy aws
/full-stack-generator devops deploy gcp
/full-stack-generator devops deploy azure
/full-stack-generator devops deploy vercel
/full-stack-generator devops deploy railway
/full-stack-generator devops deploy fly
```

---

## Configuration Options

### Project Configuration

The generator uses a `.fullstack.yaml` configuration file:

```yaml
# Project metadata
project:
  name: my-awesome-app
  description: A full-stack web application
  version: 1.0.0
  author: Your Name
  license: MIT

# Frontend configuration
frontend:
  framework: nextjs
  version: "14.1"
  typescript: true
  package_manager: pnpm

  # UI configuration
  ui:
    styling: tailwind
    component_library: shadcn
    icons: lucide
    fonts:
      - Inter
      - JetBrains Mono
    dark_mode: true

  # State management
  state:
    solution: zustand
    persist: true
    devtools: true

  # Routing
  routing:
    type: app-router
    middleware: true
    i18n:
      enabled: true
      locales:
        - en
        - zh-TW
        - ja
      default: en

  # Forms
  forms:
    library: react-hook-form
    validation: zod

  # API client
  api:
    client: tanstack-query
    base_url: /api
    retry: true
    cache: true

  # Testing
  testing:
    unit:
      framework: jest
      coverage: 80
    component:
      framework: testing-library
    e2e:
      framework: playwright
      browsers:
        - chromium
        - firefox
        - webkit

  # Build
  build:
    output: standalone
    analyze: true
    sourcemaps: false

# Backend configuration
backend:
  framework: nestjs
  version: "10.3"
  typescript: true
  package_manager: pnpm

  # Architecture
  architecture:
    pattern: clean
    modules:
      - users
      - auth
      - products
      - orders

  # API
  api:
    type: rest
    versioning: true
    prefix: /api/v1
    documentation:
      enabled: true
      path: /docs

  # Validation
  validation:
    library: class-validator
    transform: true
    whitelist: true

  # Authentication
  authentication:
    strategy: jwt
    providers:
      - local
      - google
      - github
    jwt:
      access_token_ttl: 15m
      refresh_token_ttl: 7d
    oauth:
      callback_url: /auth/callback

  # Database
  database:
    orm: prisma
    type: postgresql
    host: localhost
    port: 5432
    name: myapp
    ssl: false
    pool:
      min: 2
      max: 10
    migrations:
      auto: true

  # Caching
  caching:
    enabled: true
    store: redis
    ttl: 3600
    host: localhost
    port: 6379

  # Queue
  queue:
    enabled: true
    driver: bull
    redis:
      host: localhost
      port: 6379
    queues:
      - emails
      - notifications
      - reports

  # Logging
  logging:
    level: info
    format: json
    transports:
      - console
      - file
    file:
      path: logs/app.log
      rotate: true
      max_size: 10MB
      max_files: 5

  # Security
  security:
    helmet: true
    cors:
      enabled: true
      origins:
        - http://localhost:3000
        - https://myapp.com
    rate_limit:
      enabled: true
      window: 15m
      max_requests: 100
    csrf: true

  # Testing
  testing:
    unit:
      framework: jest
      coverage: 80
    integration:
      framework: supertest
    e2e:
      framework: jest
      database: test

# Database models
models:
  User:
    fields:
      id: uuid
      email: string @unique
      password: string
      name: string?
      avatar: string?
      role: enum(USER, ADMIN)
      emailVerified: boolean @default(false)
      createdAt: datetime
      updatedAt: datetime
    relations:
      posts: Post[]
      orders: Order[]
    indexes:
      - email

  Post:
    fields:
      id: uuid
      title: string
      content: text
      published: boolean @default(false)
      authorId: uuid
      createdAt: datetime
      updatedAt: datetime
    relations:
      author: User
      categories: Category[]
    indexes:
      - authorId
      - published

  Product:
    fields:
      id: uuid
      name: string
      description: text
      price: decimal(10,2)
      stock: integer @default(0)
      sku: string @unique
      images: json
      active: boolean @default(true)
      createdAt: datetime
      updatedAt: datetime
    relations:
      categories: Category[]
      orderItems: OrderItem[]
    indexes:
      - sku
      - active

  Order:
    fields:
      id: uuid
      userId: uuid
      status: enum(PENDING, PROCESSING, SHIPPED, DELIVERED, CANCELLED)
      total: decimal(10,2)
      shippingAddress: json
      createdAt: datetime
      updatedAt: datetime
    relations:
      user: User
      items: OrderItem[]
    indexes:
      - userId
      - status

  OrderItem:
    fields:
      id: uuid
      orderId: uuid
      productId: uuid
      quantity: integer
      price: decimal(10,2)
    relations:
      order: Order
      product: Product

  Category:
    fields:
      id: uuid
      name: string
      slug: string @unique
      description: text?
      parentId: uuid?
    relations:
      parent: Category?
      children: Category[]
      products: Product[]
      posts: Post[]

# DevOps configuration
devops:
  # Docker
  docker:
    enabled: true
    registry: ghcr.io
    compose:
      version: "3.8"
      services:
        - app
        - db
        - redis
        - nginx

  # CI/CD
  ci:
    platform: github-actions
    branches:
      main:
        - lint
        - test
        - build
        - deploy
      develop:
        - lint
        - test
        - build
      feature/*:
        - lint
        - test
    environments:
      staging:
        branch: develop
        auto_deploy: true
      production:
        branch: main
        auto_deploy: false
        approval_required: true

  # Deployment
  deployment:
    target: aws
    region: us-east-1
    services:
      frontend:
        type: cloudfront
        origin: s3
      backend:
        type: ecs
        cluster: myapp-cluster
        service: myapp-api
      database:
        type: rds
        instance: db.t3.micro
      cache:
        type: elasticache
        node: cache.t3.micro

  # Monitoring
  monitoring:
    enabled: true
    apm: datadog
    logging: cloudwatch
    alerts:
      - type: error_rate
        threshold: 5%
        channel: slack
      - type: latency
        threshold: 500ms
        channel: email

# Environment variables
environment:
  development:
    NODE_ENV: development
    DATABASE_URL: postgresql://localhost:5432/myapp_dev
    REDIS_URL: redis://localhost:6379
    JWT_SECRET: dev-secret-key

  staging:
    NODE_ENV: staging
    DATABASE_URL: ${DATABASE_URL}
    REDIS_URL: ${REDIS_URL}
    JWT_SECRET: ${JWT_SECRET}

  production:
    NODE_ENV: production
    DATABASE_URL: ${DATABASE_URL}
    REDIS_URL: ${REDIS_URL}
    JWT_SECRET: ${JWT_SECRET}
```

---

## Generation Phases

The generator follows a structured multi-phase approach to ensure complete and correct project generation:

### Phase 1: Project Initialization

During this phase, the generator performs the following tasks:

1. **Directory Structure Creation**
   - Create root project directory
   - Create subdirectories for frontend, backend, shared, docs
   - Create configuration directories

2. **Version Control Setup**
   - Initialize Git repository
   - Create `.gitignore` with appropriate patterns
   - Create initial commit

3. **Package Manager Configuration**
   - Set up monorepo structure (optional)
   - Create root `package.json` or equivalent
   - Configure workspaces

4. **Environment Configuration**
   - Create `.env.example` template
   - Create environment-specific configurations
   - Set up secret management

Example output:

```
Creating project structure...
✓ Created directory: my-awesome-app/
✓ Created directory: my-awesome-app/frontend/
✓ Created directory: my-awesome-app/backend/
✓ Created directory: my-awesome-app/shared/
✓ Created directory: my-awesome-app/docs/
✓ Initialized Git repository
✓ Created .gitignore
✓ Created package.json
✓ Created .env.example
```

### Phase 2: Frontend Generation

During this phase, the generator creates the complete frontend application:

1. **Framework Setup**
   - Install framework dependencies
   - Configure TypeScript
   - Set up build tools

2. **Component Library**
   - Install UI component library
   - Configure theme and styling
   - Create base components

3. **State Management**
   - Set up state management solution
   - Create initial stores
   - Configure devtools

4. **Routing**
   - Configure router
   - Create route definitions
   - Set up navigation guards

5. **API Integration**
   - Set up API client
   - Create API hooks/composables
   - Configure request/response interceptors

6. **Testing**
   - Install testing dependencies
   - Create test utilities
   - Write example tests

Example output:

```
Generating frontend...
✓ Installed Next.js 14.1
✓ Configured TypeScript
✓ Installed Tailwind CSS
✓ Installed shadcn/ui components
✓ Set up Zustand store
✓ Configured TanStack Query
✓ Created authentication context
✓ Created layout components
✓ Created example pages
✓ Set up Jest and Playwright
```

### Phase 3: Backend Generation

During this phase, the generator creates the complete backend application:

1. **Framework Setup**
   - Install framework dependencies
   - Configure TypeScript/language settings
   - Set up project structure

2. **Database Integration**
   - Install ORM/database driver
   - Create database configuration
   - Generate initial models/entities
   - Create migrations

3. **Authentication**
   - Set up authentication strategy
   - Create auth middleware
   - Generate auth endpoints
   - Configure session/token management

4. **API Structure**
   - Create controller/handler layer
   - Create service layer
   - Create repository layer
   - Set up dependency injection

5. **Validation**
   - Configure validation library
   - Create validation schemas
   - Set up validation middleware

6. **Documentation**
   - Set up API documentation
   - Generate OpenAPI spec
   - Create documentation UI

7. **Testing**
   - Install testing dependencies
   - Create test utilities
   - Write example tests

Example output:

```
Generating backend...
✓ Installed NestJS 10.3
✓ Configured TypeScript
✓ Installed Prisma ORM
✓ Created database schema
✓ Generated migrations
✓ Set up JWT authentication
✓ Created user module
✓ Created auth module
✓ Created product module
✓ Created order module
✓ Set up Swagger documentation
✓ Set up Jest testing
```

### Phase 4: Integration

During this phase, the generator connects frontend and backend:

1. **API Contract**
   - Generate API types from OpenAPI spec
   - Create shared type definitions
   - Validate API compatibility

2. **Environment Configuration**
   - Link frontend to backend URL
   - Configure CORS
   - Set up proxy for development

3. **Authentication Flow**
   - Connect frontend auth to backend
   - Set up token refresh
   - Configure protected routes

Example output:

```
Integrating frontend and backend...
✓ Generated API types from OpenAPI spec
✓ Created shared types package
✓ Configured development proxy
✓ Set up authentication flow
✓ Validated API compatibility
```

### Phase 5: DevOps Configuration

During this phase, the generator creates deployment and CI/CD configurations:

1. **Docker**
   - Create Dockerfiles
   - Create docker-compose files
   - Configure multi-stage builds

2. **CI/CD**
   - Create CI pipeline configuration
   - Set up automated testing
   - Configure deployment workflows

3. **Infrastructure**
   - Create infrastructure as code (optional)
   - Configure cloud resources
   - Set up monitoring

Example output:

```
Generating DevOps configuration...
✓ Created Dockerfile for frontend
✓ Created Dockerfile for backend
✓ Created docker-compose.yml
✓ Created docker-compose.prod.yml
✓ Created GitHub Actions workflow
✓ Created deployment scripts
✓ Generated Terraform configuration (optional)
```

### Phase 6: Documentation

During this phase, the generator creates project documentation:

1. **README**
   - Project overview
   - Getting started guide
   - Development instructions
   - Deployment guide

2. **API Documentation**
   - Endpoint reference
   - Authentication guide
   - Error codes

3. **Architecture Documentation**
   - System overview
   - Component diagrams
   - Data flow diagrams

4. **Contributing Guide**
   - Code style guide
   - PR process
   - Testing requirements

Example output:

```
Generating documentation...
✓ Created README.md
✓ Created CONTRIBUTING.md
✓ Created API documentation
✓ Created architecture diagrams
✓ Created deployment guide
```

---

## Frontend Generation

### Directory Structure

The generated frontend follows this structure:

```
frontend/
├── public/
│   ├── favicon.ico
│   ├── robots.txt
│   └── assets/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── (auth)/
│   │   │   ├── login/
│   │   │   └── register/
│   │   ├── (dashboard)/
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx
│   │   │   ├── settings/
│   │   │   └── profile/
│   │   ├── api/
│   │   │   └── [...]/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── globals.css
│   ├── components/
│   │   ├── ui/                 # Base UI components
│   │   │   ├── button.tsx
│   │   │   ├── input.tsx
│   │   │   ├── card.tsx
│   │   │   └── ...
│   │   ├── forms/              # Form components
│   │   │   ├── login-form.tsx
│   │   │   └── ...
│   │   ├── layouts/            # Layout components
│   │   │   ├── header.tsx
│   │   │   ├── sidebar.tsx
│   │   │   └── footer.tsx
│   │   └── features/           # Feature components
│   │       ├── auth/
│   │       ├── dashboard/
│   │       └── ...
│   ├── hooks/                  # Custom hooks
│   │   ├── use-auth.ts
│   │   ├── use-api.ts
│   │   └── ...
│   ├── lib/                    # Utilities
│   │   ├── api.ts
│   │   ├── utils.ts
│   │   └── ...
│   ├── stores/                 # State management
│   │   ├── auth-store.ts
│   │   └── ...
│   ├── types/                  # TypeScript types
│   │   ├── api.ts
│   │   └── ...
│   └── styles/                 # Global styles
│       └── ...
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── .env.example
├── .env.local
├── next.config.js
├── tailwind.config.js
├── tsconfig.json
├── jest.config.js
├── playwright.config.ts
└── package.json
```

### Component Generation

Components are generated with the following structure:

```typescript
// components/ui/button.tsx
import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const buttonVariants = cva(
  "inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90",
        outline: "border border-input bg-background hover:bg-accent hover:text-accent-foreground",
        secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/80",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 rounded-md px-3",
        lg: "h-11 rounded-md px-8",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button"
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    )
  }
)
Button.displayName = "Button"

export { Button, buttonVariants }
```

### State Management

State management is set up using the selected solution:

```typescript
// stores/auth-store.ts
import { create } from 'zustand'
import { persist, createJSONStorage } from 'zustand/middleware'
import { immer } from 'zustand/middleware/immer'

interface User {
  id: string
  email: string
  name: string
  avatar?: string
  role: 'USER' | 'ADMIN'
}

interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  isLoading: boolean

  // Actions
  setUser: (user: User) => void
  setToken: (token: string) => void
  login: (email: string, password: string) => Promise<void>
  logout: () => void
  refreshToken: () => Promise<void>
}

export const useAuthStore = create<AuthState>()(
  persist(
    immer((set, get) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      isLoading: false,

      setUser: (user) => {
        set((state) => {
          state.user = user
          state.isAuthenticated = true
        })
      },

      setToken: (token) => {
        set((state) => {
          state.token = token
        })
      },

      login: async (email, password) => {
        set((state) => { state.isLoading = true })
        try {
          const response = await fetch('/api/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password }),
          })
          const data = await response.json()
          set((state) => {
            state.user = data.user
            state.token = data.token
            state.isAuthenticated = true
            state.isLoading = false
          })
        } catch (error) {
          set((state) => { state.isLoading = false })
          throw error
        }
      },

      logout: () => {
        set((state) => {
          state.user = null
          state.token = null
          state.isAuthenticated = false
        })
      },

      refreshToken: async () => {
        try {
          const response = await fetch('/api/auth/refresh', {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${get().token}`,
            },
          })
          const data = await response.json()
          set((state) => {
            state.token = data.token
          })
        } catch (error) {
          get().logout()
          throw error
        }
      },
    })),
    {
      name: 'auth-storage',
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({ token: state.token }),
    }
  )
)
```

---

## Backend Generation

### Directory Structure

The generated backend follows this structure:

```
backend/
├── src/
│   ├── app.module.ts
│   ├── main.ts
│   ├── common/
│   │   ├── decorators/
│   │   ├── filters/
│   │   ├── guards/
│   │   ├── interceptors/
│   │   ├── pipes/
│   │   └── utils/
│   ├── config/
│   │   ├── app.config.ts
│   │   ├── database.config.ts
│   │   └── jwt.config.ts
│   ├── modules/
│   │   ├── auth/
│   │   │   ├── auth.module.ts
│   │   │   ├── auth.controller.ts
│   │   │   ├── auth.service.ts
│   │   │   ├── strategies/
│   │   │   ├── guards/
│   │   │   └── dto/
│   │   ├── users/
│   │   │   ├── users.module.ts
│   │   │   ├── users.controller.ts
│   │   │   ├── users.service.ts
│   │   │   ├── users.repository.ts
│   │   │   ├── entities/
│   │   │   └── dto/
│   │   ├── products/
│   │   │   └── ...
│   │   └── orders/
│   │       └── ...
│   └── database/
│       ├── prisma/
│       │   ├── schema.prisma
│       │   └── migrations/
│       └── seeds/
├── test/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── .env.example
├── .env
├── nest-cli.json
├── tsconfig.json
├── tsconfig.build.json
├── jest.config.js
└── package.json
```

### Module Generation

Modules are generated with the following structure:

```typescript
// modules/users/users.module.ts
import { Module } from '@nestjs/common'
import { UsersController } from './users.controller'
import { UsersService } from './users.service'
import { UsersRepository } from './users.repository'
import { PrismaModule } from '@/database/prisma/prisma.module'

@Module({
  imports: [PrismaModule],
  controllers: [UsersController],
  providers: [UsersService, UsersRepository],
  exports: [UsersService],
})
export class UsersModule {}

// modules/users/users.controller.ts
import {
  Controller,
  Get,
  Post,
  Put,
  Delete,
  Body,
  Param,
  Query,
  UseGuards,
  ParseUUIDPipe,
} from '@nestjs/common'
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger'
import { JwtAuthGuard } from '@/common/guards/jwt-auth.guard'
import { RolesGuard } from '@/common/guards/roles.guard'
import { Roles } from '@/common/decorators/roles.decorator'
import { CurrentUser } from '@/common/decorators/current-user.decorator'
import { UsersService } from './users.service'
import { CreateUserDto, UpdateUserDto, UserQueryDto } from './dto'
import { User, Role } from '@prisma/client'

@ApiTags('users')
@Controller('users')
@UseGuards(JwtAuthGuard, RolesGuard)
@ApiBearerAuth()
export class UsersController {
  constructor(private readonly usersService: UsersService) {}

  @Post()
  @Roles(Role.ADMIN)
  @ApiOperation({ summary: 'Create a new user' })
  async create(@Body() createUserDto: CreateUserDto) {
    return this.usersService.create(createUserDto)
  }

  @Get()
  @ApiOperation({ summary: 'Get all users' })
  async findAll(@Query() query: UserQueryDto) {
    return this.usersService.findAll(query)
  }

  @Get('me')
  @ApiOperation({ summary: 'Get current user profile' })
  async getProfile(@CurrentUser() user: User) {
    return this.usersService.findById(user.id)
  }

  @Get(':id')
  @ApiOperation({ summary: 'Get user by ID' })
  async findOne(@Param('id', ParseUUIDPipe) id: string) {
    return this.usersService.findById(id)
  }

  @Put(':id')
  @ApiOperation({ summary: 'Update user' })
  async update(
    @Param('id', ParseUUIDPipe) id: string,
    @Body() updateUserDto: UpdateUserDto,
    @CurrentUser() currentUser: User,
  ) {
    return this.usersService.update(id, updateUserDto, currentUser)
  }

  @Delete(':id')
  @Roles(Role.ADMIN)
  @ApiOperation({ summary: 'Delete user' })
  async remove(@Param('id', ParseUUIDPipe) id: string) {
    return this.usersService.remove(id)
  }
}

// modules/users/users.service.ts
import {
  Injectable,
  NotFoundException,
  ForbiddenException,
} from '@nestjs/common'
import { UsersRepository } from './users.repository'
import { CreateUserDto, UpdateUserDto, UserQueryDto } from './dto'
import { User, Role } from '@prisma/client'
import * as bcrypt from 'bcrypt'

@Injectable()
export class UsersService {
  constructor(private readonly usersRepository: UsersRepository) {}

  async create(createUserDto: CreateUserDto) {
    const hashedPassword = await bcrypt.hash(createUserDto.password, 10)
    return this.usersRepository.create({
      ...createUserDto,
      password: hashedPassword,
    })
  }

  async findAll(query: UserQueryDto) {
    return this.usersRepository.findAll(query)
  }

  async findById(id: string) {
    const user = await this.usersRepository.findById(id)
    if (!user) {
      throw new NotFoundException(`User with ID ${id} not found`)
    }
    return user
  }

  async findByEmail(email: string) {
    return this.usersRepository.findByEmail(email)
  }

  async update(id: string, updateUserDto: UpdateUserDto, currentUser: User) {
    const user = await this.findById(id)

    // Only admins can update other users
    if (user.id !== currentUser.id && currentUser.role !== Role.ADMIN) {
      throw new ForbiddenException('You can only update your own profile')
    }

    if (updateUserDto.password) {
      updateUserDto.password = await bcrypt.hash(updateUserDto.password, 10)
    }

    return this.usersRepository.update(id, updateUserDto)
  }

  async remove(id: string) {
    await this.findById(id)
    return this.usersRepository.remove(id)
  }
}

// modules/users/users.repository.ts
import { Injectable } from '@nestjs/common'
import { PrismaService } from '@/database/prisma/prisma.service'
import { CreateUserDto, UpdateUserDto, UserQueryDto } from './dto'
import { Prisma } from '@prisma/client'

@Injectable()
export class UsersRepository {
  constructor(private readonly prisma: PrismaService) {}

  async create(data: CreateUserDto) {
    return this.prisma.user.create({
      data,
      select: {
        id: true,
        email: true,
        name: true,
        avatar: true,
        role: true,
        createdAt: true,
      },
    })
  }

  async findAll(query: UserQueryDto) {
    const { page = 1, limit = 10, search, role, sortBy, sortOrder } = query

    const where: Prisma.UserWhereInput = {}

    if (search) {
      where.OR = [
        { email: { contains: search, mode: 'insensitive' } },
        { name: { contains: search, mode: 'insensitive' } },
      ]
    }

    if (role) {
      where.role = role
    }

    const [users, total] = await Promise.all([
      this.prisma.user.findMany({
        where,
        select: {
          id: true,
          email: true,
          name: true,
          avatar: true,
          role: true,
          createdAt: true,
        },
        skip: (page - 1) * limit,
        take: limit,
        orderBy: sortBy ? { [sortBy]: sortOrder || 'asc' } : { createdAt: 'desc' },
      }),
      this.prisma.user.count({ where }),
    ])

    return {
      data: users,
      meta: {
        total,
        page,
        limit,
        totalPages: Math.ceil(total / limit),
      },
    }
  }

  async findById(id: string) {
    return this.prisma.user.findUnique({
      where: { id },
      select: {
        id: true,
        email: true,
        name: true,
        avatar: true,
        role: true,
        emailVerified: true,
        createdAt: true,
        updatedAt: true,
      },
    })
  }

  async findByEmail(email: string) {
    return this.prisma.user.findUnique({
      where: { email },
    })
  }

  async update(id: string, data: UpdateUserDto) {
    return this.prisma.user.update({
      where: { id },
      data,
      select: {
        id: true,
        email: true,
        name: true,
        avatar: true,
        role: true,
        updatedAt: true,
      },
    })
  }

  async remove(id: string) {
    return this.prisma.user.delete({
      where: { id },
    })
  }
}
```

---

## Database Setup

### Prisma Schema

The generator creates a comprehensive Prisma schema:

```prisma
// database/prisma/schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

enum Role {
  USER
  ADMIN
}

enum OrderStatus {
  PENDING
  PROCESSING
  SHIPPED
  DELIVERED
  CANCELLED
}

model User {
  id            String    @id @default(uuid())
  email         String    @unique
  password      String
  name          String?
  avatar        String?
  role          Role      @default(USER)
  emailVerified Boolean   @default(false)
  createdAt     DateTime  @default(now())
  updatedAt     DateTime  @updatedAt

  posts         Post[]
  orders        Order[]
  refreshTokens RefreshToken[]

  @@index([email])
}

model RefreshToken {
  id        String   @id @default(uuid())
  token     String   @unique
  userId    String
  expiresAt DateTime
  createdAt DateTime @default(now())

  user User @relation(fields: [userId], references: [id], onDelete: Cascade)

  @@index([userId])
  @@index([token])
}

model Post {
  id        String   @id @default(uuid())
  title     String
  content   String
  published Boolean  @default(false)
  authorId  String
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  author     User       @relation(fields: [authorId], references: [id], onDelete: Cascade)
  categories Category[]

  @@index([authorId])
  @@index([published])
}

model Product {
  id          String   @id @default(uuid())
  name        String
  description String
  price       Decimal  @db.Decimal(10, 2)
  stock       Int      @default(0)
  sku         String   @unique
  images      Json     @default("[]")
  active      Boolean  @default(true)
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt

  categories Category[]
  orderItems OrderItem[]

  @@index([sku])
  @@index([active])
}

model Order {
  id              String      @id @default(uuid())
  userId          String
  status          OrderStatus @default(PENDING)
  total           Decimal     @db.Decimal(10, 2)
  shippingAddress Json
  createdAt       DateTime    @default(now())
  updatedAt       DateTime    @updatedAt

  user  User        @relation(fields: [userId], references: [id], onDelete: Cascade)
  items OrderItem[]

  @@index([userId])
  @@index([status])
}

model OrderItem {
  id        String  @id @default(uuid())
  orderId   String
  productId String
  quantity  Int
  price     Decimal @db.Decimal(10, 2)

  order   Order   @relation(fields: [orderId], references: [id], onDelete: Cascade)
  product Product @relation(fields: [productId], references: [id])

  @@index([orderId])
  @@index([productId])
}

model Category {
  id          String  @id @default(uuid())
  name        String
  slug        String  @unique
  description String?
  parentId    String?

  parent   Category?  @relation("CategoryParent", fields: [parentId], references: [id])
  children Category[] @relation("CategoryParent")
  products Product[]
  posts    Post[]

  @@index([slug])
  @@index([parentId])
}
```

---

## Authentication

### JWT Authentication Implementation

The generator creates a complete JWT authentication system:

```typescript
// modules/auth/auth.service.ts
import {
  Injectable,
  UnauthorizedException,
  ConflictException,
} from '@nestjs/common'
import { JwtService } from '@nestjs/jwt'
import { ConfigService } from '@nestjs/config'
import { UsersService } from '@/modules/users/users.service'
import { PrismaService } from '@/database/prisma/prisma.service'
import { RegisterDto, LoginDto } from './dto'
import * as bcrypt from 'bcrypt'
import { v4 as uuidv4 } from 'uuid'

@Injectable()
export class AuthService {
  constructor(
    private readonly usersService: UsersService,
    private readonly jwtService: JwtService,
    private readonly configService: ConfigService,
    private readonly prisma: PrismaService,
  ) {}

  async register(registerDto: RegisterDto) {
    const existingUser = await this.usersService.findByEmail(registerDto.email)
    if (existingUser) {
      throw new ConflictException('Email already registered')
    }

    const hashedPassword = await bcrypt.hash(registerDto.password, 10)
    const user = await this.prisma.user.create({
      data: {
        ...registerDto,
        password: hashedPassword,
      },
    })

    const tokens = await this.generateTokens(user.id, user.email)
    await this.saveRefreshToken(user.id, tokens.refreshToken)

    return {
      user: {
        id: user.id,
        email: user.email,
        name: user.name,
        role: user.role,
      },
      ...tokens,
    }
  }

  async login(loginDto: LoginDto) {
    const user = await this.usersService.findByEmail(loginDto.email)
    if (!user) {
      throw new UnauthorizedException('Invalid credentials')
    }

    const isPasswordValid = await bcrypt.compare(loginDto.password, user.password)
    if (!isPasswordValid) {
      throw new UnauthorizedException('Invalid credentials')
    }

    const tokens = await this.generateTokens(user.id, user.email)
    await this.saveRefreshToken(user.id, tokens.refreshToken)

    return {
      user: {
        id: user.id,
        email: user.email,
        name: user.name,
        role: user.role,
      },
      ...tokens,
    }
  }

  async refreshTokens(refreshToken: string) {
    const storedToken = await this.prisma.refreshToken.findUnique({
      where: { token: refreshToken },
      include: { user: true },
    })

    if (!storedToken || storedToken.expiresAt < new Date()) {
      throw new UnauthorizedException('Invalid refresh token')
    }

    // Delete old refresh token
    await this.prisma.refreshToken.delete({
      where: { id: storedToken.id },
    })

    // Generate new tokens
    const tokens = await this.generateTokens(
      storedToken.user.id,
      storedToken.user.email,
    )
    await this.saveRefreshToken(storedToken.user.id, tokens.refreshToken)

    return tokens
  }

  async logout(userId: string, refreshToken: string) {
    await this.prisma.refreshToken.deleteMany({
      where: {
        userId,
        token: refreshToken,
      },
    })
  }

  private async generateTokens(userId: string, email: string) {
    const [accessToken, refreshToken] = await Promise.all([
      this.jwtService.signAsync(
        { sub: userId, email },
        {
          secret: this.configService.get('JWT_ACCESS_SECRET'),
          expiresIn: this.configService.get('JWT_ACCESS_TTL', '15m'),
        },
      ),
      this.jwtService.signAsync(
        { sub: userId, email, jti: uuidv4() },
        {
          secret: this.configService.get('JWT_REFRESH_SECRET'),
          expiresIn: this.configService.get('JWT_REFRESH_TTL', '7d'),
        },
      ),
    ])

    return { accessToken, refreshToken }
  }

  private async saveRefreshToken(userId: string, token: string) {
    const decoded = this.jwtService.decode(token) as { exp: number }
    const expiresAt = new Date(decoded.exp * 1000)

    await this.prisma.refreshToken.create({
      data: {
        token,
        userId,
        expiresAt,
      },
    })
  }
}
```

---

## Testing Setup

### Unit Testing

```typescript
// test/unit/users.service.spec.ts
import { Test, TestingModule } from '@nestjs/testing'
import { UsersService } from '@/modules/users/users.service'
import { UsersRepository } from '@/modules/users/users.repository'
import { NotFoundException, ForbiddenException } from '@nestjs/common'
import { Role } from '@prisma/client'

describe('UsersService', () => {
  let service: UsersService
  let repository: jest.Mocked<UsersRepository>

  const mockUser = {
    id: 'user-id',
    email: 'test@example.com',
    name: 'Test User',
    avatar: null,
    role: Role.USER,
    emailVerified: false,
    createdAt: new Date(),
    updatedAt: new Date(),
  }

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        UsersService,
        {
          provide: UsersRepository,
          useValue: {
            create: jest.fn(),
            findAll: jest.fn(),
            findById: jest.fn(),
            findByEmail: jest.fn(),
            update: jest.fn(),
            remove: jest.fn(),
          },
        },
      ],
    }).compile()

    service = module.get<UsersService>(UsersService)
    repository = module.get(UsersRepository)
  })

  describe('findById', () => {
    it('should return a user when found', async () => {
      repository.findById.mockResolvedValue(mockUser)

      const result = await service.findById('user-id')

      expect(result).toEqual(mockUser)
      expect(repository.findById).toHaveBeenCalledWith('user-id')
    })

    it('should throw NotFoundException when user not found', async () => {
      repository.findById.mockResolvedValue(null)

      await expect(service.findById('nonexistent')).rejects.toThrow(
        NotFoundException,
      )
    })
  })

  describe('update', () => {
    it('should allow users to update their own profile', async () => {
      repository.findById.mockResolvedValue(mockUser)
      repository.update.mockResolvedValue({ ...mockUser, name: 'Updated Name' })

      const result = await service.update(
        'user-id',
        { name: 'Updated Name' },
        mockUser,
      )

      expect(result.name).toBe('Updated Name')
    })

    it('should throw ForbiddenException when updating other user profile', async () => {
      repository.findById.mockResolvedValue(mockUser)

      const otherUser = { ...mockUser, id: 'other-user-id' }

      await expect(
        service.update('user-id', { name: 'Hacked' }, otherUser),
      ).rejects.toThrow(ForbiddenException)
    })

    it('should allow admins to update any user', async () => {
      repository.findById.mockResolvedValue(mockUser)
      repository.update.mockResolvedValue({ ...mockUser, name: 'Admin Updated' })

      const adminUser = { ...mockUser, id: 'admin-id', role: Role.ADMIN }

      const result = await service.update(
        'user-id',
        { name: 'Admin Updated' },
        adminUser,
      )

      expect(result.name).toBe('Admin Updated')
    })
  })
})
```

### E2E Testing

```typescript
// test/e2e/auth.e2e-spec.ts
import { Test, TestingModule } from '@nestjs/testing'
import { INestApplication, ValidationPipe } from '@nestjs/common'
import * as request from 'supertest'
import { AppModule } from '@/app.module'
import { PrismaService } from '@/database/prisma/prisma.service'

describe('Auth (e2e)', () => {
  let app: INestApplication
  let prisma: PrismaService

  beforeAll(async () => {
    const moduleFixture: TestingModule = await Test.createTestingModule({
      imports: [AppModule],
    }).compile()

    app = moduleFixture.createNestApplication()
    app.useGlobalPipes(new ValidationPipe({ transform: true }))
    await app.init()

    prisma = app.get(PrismaService)
  })

  afterAll(async () => {
    await prisma.user.deleteMany()
    await app.close()
  })

  describe('POST /auth/register', () => {
    it('should register a new user', async () => {
      const response = await request(app.getHttpServer())
        .post('/auth/register')
        .send({
          email: 'test@example.com',
          password: 'Password123!',
          name: 'Test User',
        })
        .expect(201)

      expect(response.body).toHaveProperty('accessToken')
      expect(response.body).toHaveProperty('refreshToken')
      expect(response.body.user.email).toBe('test@example.com')
    })

    it('should return 409 for duplicate email', async () => {
      await request(app.getHttpServer())
        .post('/auth/register')
        .send({
          email: 'test@example.com',
          password: 'Password123!',
          name: 'Another User',
        })
        .expect(409)
    })
  })

  describe('POST /auth/login', () => {
    it('should login with valid credentials', async () => {
      const response = await request(app.getHttpServer())
        .post('/auth/login')
        .send({
          email: 'test@example.com',
          password: 'Password123!',
        })
        .expect(200)

      expect(response.body).toHaveProperty('accessToken')
      expect(response.body).toHaveProperty('refreshToken')
    })

    it('should return 401 for invalid credentials', async () => {
      await request(app.getHttpServer())
        .post('/auth/login')
        .send({
          email: 'test@example.com',
          password: 'WrongPassword',
        })
        .expect(401)
    })
  })
})
```

---

## CI/CD Configuration

### GitHub Actions

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v2
        with:
          version: 8
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'pnpm'
      - run: pnpm install
      - run: pnpm lint

  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
      redis:
        image: redis:7
        ports:
          - 6379:6379
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v2
        with:
          version: 8
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'pnpm'
      - run: pnpm install
      - run: pnpm test:cov
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/test
          REDIS_URL: redis://localhost:6379
      - uses: codecov/codecov-action@v3

  build:
    runs-on: ubuntu-latest
    needs: [lint, test]
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v2
        with:
          version: 8
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'pnpm'
      - run: pnpm install
      - run: pnpm build

  deploy:
    runs-on: ubuntu-latest
    needs: [build]
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to production
        run: echo "Deploying to production..."
```

---

## Deployment

### Docker Configuration

```dockerfile
# Dockerfile
FROM node:20-alpine AS base
RUN npm install -g pnpm

FROM base AS deps
WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN pnpm build

FROM base AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY package.json ./
EXPOSE 3000
CMD ["node", "dist/main.js"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build: .
    ports:
      - '3000:3000'
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/myapp
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=myapp
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - '5432:5432'

  redis:
    image: redis:7-alpine
    ports:
      - '6379:6379'
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

---

## Examples

### Example 1: Create a SaaS Application

```bash
/full-stack-generator init my-saas-app \
  --frontend nextjs \
  --backend nestjs \
  --database postgresql \
  --auth jwt \
  --features subscription,teams,billing
```

### Example 2: Create an E-commerce Platform

```bash
/full-stack-generator init my-shop \
  --frontend nuxt \
  --backend fastapi \
  --database postgresql \
  --auth oauth2 \
  --features products,cart,checkout,payments
```

### Example 3: Create a Blog Platform

```bash
/full-stack-generator init my-blog \
  --frontend sveltekit \
  --backend express \
  --database mongodb \
  --auth session \
  --features posts,comments,tags
```

---

## Troubleshooting

### Common Issues

#### Issue: Database connection failed

**Solution**: Ensure the database is running and the connection string is correct:

```bash
# Check database status
docker-compose ps

# Check connection string
echo $DATABASE_URL

# Test connection
npx prisma db push
```

#### Issue: Authentication not working

**Solution**: Verify JWT configuration:

```bash
# Check environment variables
echo $JWT_ACCESS_SECRET
echo $JWT_REFRESH_SECRET

# Regenerate secrets
node -e "console.log(require('crypto').randomBytes(64).toString('hex'))"
```

#### Issue: Build failing

**Solution**: Clear cache and rebuild:

```bash
# Clear node_modules
rm -rf node_modules
pnpm install

# Clear build cache
rm -rf .next dist
pnpm build
```

---

## Related Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [NestJS Documentation](https://docs.nestjs.com)
- [Prisma Documentation](https://www.prisma.io/docs)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)

---

Made with Claude Code by [Claude World](https://claude-world.com)
