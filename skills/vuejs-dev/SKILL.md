---
name: vuejs-dev
description: >-
  Vue.js / Vite / Node.js development workflow in Docker: Vite dev server, production
  build, Vitest unit tests, vue-tsc TypeScript type checking, ESLint linting, npm
  package management. Use when working with the frontend service, running frontend
  tests, checking types, or managing npm dependencies.
---

# Vue.js Development Workflow

<!-- cs: Workflow pro vývoj Vue.js / Node.js v Dockeru -->

## Prerequisites

<!-- cs: Předpoklady -->

- Check `docker-compose.yml` for the frontend service name (commonly `frontend`, `web`, `ui`).
  <!-- cs: Zkontroluj docker-compose.yml pro název frontend služby (typicky frontend, web, ui). -->
- Vite dev server is typically started automatically on `docker compose up`.
  <!-- cs: Vite dev server se typicky spouští automaticky přes docker compose up. -->

## Development Server

<!-- cs: Dev server -->

```bash
# Start all services (includes Vite dev server)
docker compose up

# Start frontend service only
docker compose up <service>

# Dev server is accessible at http://localhost:5173 (Vite default).
# Check docker-compose.yml for the actual mapped port.
```

## Build

<!-- cs: Build -->

```bash
# Production build (output in dist/)
docker compose exec <service> npm run build

# Preview production build locally
docker compose exec <service> npm run preview
```

## Testing (Vitest)

<!-- cs: Testování (Vitest) -->

```bash
# Run all tests once
docker compose exec <service> npx vitest run

# Watch mode — reruns on file change (use during development)
docker compose exec -it <service> npx vitest

# Verbose output
docker compose exec <service> npx vitest run --reporter=verbose

# Single test file
docker compose exec <service> npx vitest run src/components/UserCard.test.ts

# Coverage report
docker compose exec <service> npx vitest run --coverage
```

## Type Checking (vue-tsc)

<!-- cs: Kontrola typů (vue-tsc) -->

```bash
# Full type check, no emit
docker compose exec <service> npx vue-tsc --noEmit

# Watch mode
docker compose exec -it <service> npx vue-tsc --noEmit --watch
```

## Linting (ESLint)

<!-- cs: Linting (ESLint) -->

```bash
# Lint src/ directory
docker compose exec <service> npx eslint src/

# Auto-fix fixable issues
docker compose exec <service> npx eslint src/ --fix

# Single file
docker compose exec <service> npx eslint src/components/UserCard.vue
```

## Full Quality Gate

<!-- cs: Plná kontrola před commitem -->

```bash
docker compose exec <service> npx vue-tsc --noEmit \
  && docker compose exec <service> npx eslint src/ \
  && docker compose exec <service> npx vitest run
```

## Package Management

<!-- cs: Správa balíčků -->

```bash
# Install a runtime dependency
docker compose exec <service> npm install <package>

# Install a dev dependency
docker compose exec <service> npm install -D <package>

# After any package.json change — rebuild image and restart
docker compose build <service>
docker compose up -d <service>
```

> `node_modules` live inside the Docker image, not in a bind-mounted local folder.
> Any `npm install` inside a running container is lost on restart.
> Always rebuild after changing `package.json`.
> <!-- cs: node_modules jsou uvnitř Docker image, ne v lokálním adresáři. npm install v běžícím kontejneru je ztracen po restartu. Po změně package.json vždy rebuilduj. -->

## Container Shell

<!-- cs: Shell kontejneru -->

```bash
# Alpine-based images (most Node.js images)
docker compose exec -it <service> sh

# Debian-based images
docker compose exec -it <service> bash
```
