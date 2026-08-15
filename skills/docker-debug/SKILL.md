---
name: docker-debug
description: >-
  Diagnose and fix Docker and Docker Compose issues: container not starting,
  unhealthy services, build failures, volume permissions, port conflicts, and
  networking problems. Use when a Docker container crashes, fails to build,
  or a service is stuck in unhealthy state.
---

# Docker Debugging

## Step 1 — Get the full picture

```bash
docker compose ps                      # status and health of all services
docker compose logs --tail=100         # recent logs from all services
docker compose logs --tail=100 <svc>   # logs for one specific service
docker inspect <container_id>          # full container metadata and config
```

## Step 2 — Diagnose by symptom

### Container exits immediately

```bash
docker compose logs <service>          # read the error message
docker run --rm -it <image> sh         # start interactively — bypass CMD
```

Common causes:

- Missing environment variable → check `.env` and `env_file` in compose
- Application crash on startup → read the stack trace in logs
- Wrong `CMD` or `ENTRYPOINT` path

### Service stuck in `unhealthy`

```bash
docker inspect --format='{{json .State.Health}}' <container> | python -m json.tool
```

Common causes:

- Service not ready within `start-period` → increase `start-period` in healthcheck
- Wrong healthcheck command or port
- Missing `curl` or `pg_isready` in the image

### Build failure

```bash
docker compose build --no-cache <svc>  # force full rebuild
docker build --progress=plain .        # verbose output — see exact failing step
```

Common causes:

- Package not found → check pinned version exists in registry
- Network error during build → retry; check proxy settings
- `.dockerignore` excluding a required file

### Port already in use

```bash
ss -tlnp | grep <port>                 # find which process uses the port
docker compose down                    # stop all services
```

### Volume permission error

```bash
docker compose exec <svc> ls -la /path/to/volume
```

Common cause: host UID ≠ container UID — fix with `chown` in Dockerfile or explicit `user:` in compose.

### Service cannot reach another service

```bash
docker compose exec <svc> ping <other-service-name>    # test DNS resolution
docker compose exec <svc> curl http://<svc>:<port>     # test HTTP reachability
docker network ls && docker network inspect <network>  # inspect network config
```

Services reach each other by **service name**, not `localhost`.

## Step 3 — Quick fixes reference

| Problem | Fix |
|---------|-----|
| Stale image after code change | `docker compose build <svc>` |
| Stale image after dep change | `docker compose build --no-cache <svc>` |
| DB data corruption | `docker compose down -v` (⚠ deletes volumes) |
| Out of disk space | `docker system prune -f && docker volume prune -f` |
| Wrong env values | Check `.env`, verify with `docker compose config` |

## Additional resources

- [04-docker-standards.mdc](../../rules/04-docker-standards.mdc) — Dockerfile and compose standards
