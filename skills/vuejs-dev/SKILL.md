---
name: vuejs-dev
description: >-
  Vue.js / Vite / Node.js development workflow in Docker: Vite dev server, production
  build, Vitest unit tests, vue-tsc TypeScript type checking, oxlint, Playwright E2E, npm
  package management. Use when working with the frontend service, running frontend
  tests, checking types, or managing npm dependencies.
---

# Vue.js Development Workflow

## Prerequisites

- Check `docker-compose.yml` for the frontend service name (commonly `frontend`, `web`, `ui`).
- Vite dev server is typically started automatically on `docker compose up`.

## Development Server

```bash
# Start all services (includes Vite dev server)
docker compose up

# Start frontend service only
docker compose up <service>

# Dev server is accessible at http://localhost:5173 (Vite default).
# Check docker-compose.yml for the actual mapped port.
```

## Build

```bash
# Production build (output in dist/)
docker compose exec <service> npm run build

# Preview production build locally
docker compose exec <service> npm run preview
```

## Testing (Vitest)

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

```bash
# Full type check, no emit
docker compose exec <service> npx vue-tsc --noEmit

# Watch mode
docker compose exec -it <service> npx vue-tsc --noEmit --watch
```

## Linting (oxlint)

```bash
docker compose exec <service> npx oxlint src/
docker compose exec <service> npx oxlint src/ --fix
```

ESLint only for rules oxlint does not cover (`npx eslint` as an extra step, not the default).

## Full Quality Gate

```bash
docker compose exec <service> npx vue-tsc --noEmit \
  && docker compose exec <service> npx oxlint src/ \
  && docker compose exec <service> npx vitest run
```

E2E (when the app is up): `npx playwright test`

## Package Management

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

## Container Shell

```bash
# Alpine-based images (most Node.js images)
docker compose exec -it <service> sh

# Debian-based images
docker compose exec -it <service> bash
```
