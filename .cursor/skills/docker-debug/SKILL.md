---
name: docker-debug
description: >-
  Diagnose and fix Docker and Docker Compose issues: container not starting,
  unhealthy services, build failures, volume permissions, port conflicts, and
  networking problems. Use when a Docker container crashes, fails to build,
  or a service is stuck in unhealthy state.
---

# Docker Debugging

<!-- cs: Diagnostika a opravy problémů s Dockerem -->

## Step 1 — Get the full picture

<!-- cs: Krok 1 — Získej úplný přehled -->

```bash
docker compose ps                      # status and health of all services
docker compose logs --tail=100         # recent logs from all services
docker compose logs --tail=100 <svc>   # logs for one specific service
docker inspect <container_id>          # full container metadata and config
```

## Step 2 — Diagnose by symptom

<!-- cs: Krok 2 — Diagnostika podle příznaku -->

### Container exits immediately

<!-- cs: Kontejner okamžitě skončí -->

```bash
docker compose logs <service>          # read the error message
docker run --rm -it <image> sh         # start interactively — bypass CMD
```

Common causes:
<!-- cs: Časté příčiny: -->
- Missing environment variable → check `.env` and `env_file` in compose
  <!-- cs: Chybějící env proměnná → zkontroluj .env a env_file v compose -->
- Application crash on startup → read the stack trace in logs
  <!-- cs: Pád aplikace při startu → přečti stack trace v logách -->
- Wrong `CMD` or `ENTRYPOINT` path
  <!-- cs: Špatná cesta v CMD nebo ENTRYPOINT -->

### Service stuck in `unhealthy`

<!-- cs: Služba uvízlá ve stavu unhealthy -->

```bash
docker inspect --format='{{json .State.Health}}' <container> | python -m json.tool
```

Common causes:
<!-- cs: Časté příčiny: -->
- Service not ready within `start-period` → increase `start-period` in healthcheck
  <!-- cs: Služba není připravena včas → zvyš start-period v healthcheck -->
- Wrong healthcheck command or port
  <!-- cs: Špatný příkaz nebo port v healthcheck -->
- Missing `curl` or `pg_isready` in the image
  <!-- cs: Chybí curl nebo pg_isready v image -->

### Build failure

<!-- cs: Chyba při buildu -->

```bash
docker compose build --no-cache <svc>  # force full rebuild
docker build --progress=plain .        # verbose output — see exact failing step
```

Common causes:
<!-- cs: Časté příčiny: -->
- Package not found → check pinned version exists in registry
  <!-- cs: Balíček nenalezen → ověř, zda pinovaná verze existuje v registru -->
- Network error during build → retry; check proxy settings
  <!-- cs: Síťová chyba při buildu → zkus znovu; zkontroluj proxy nastavení -->
- `.dockerignore` excluding a required file
  <!-- cs: .dockerignore vylučuje potřebný soubor -->

### Port already in use

<!-- cs: Port je již obsazen -->

```bash
ss -tlnp | grep <port>                 # find which process uses the port
docker compose down                    # stop all services
```

### Volume permission error

<!-- cs: Chyba oprávnění na volume -->

```bash
docker compose exec <svc> ls -la /path/to/volume
```

Common cause: host UID ≠ container UID — fix with `chown` in Dockerfile or explicit `user:` in compose.
<!-- cs: Časté: UID hosta ≠ UID kontejneru — oprav chown v Dockerfile nebo user: v compose. -->

### Service cannot reach another service

<!-- cs: Služba nemůže dosáhnout jiné služby -->

```bash
docker compose exec <svc> ping <other-service-name>    # test DNS resolution
docker compose exec <svc> curl http://<svc>:<port>     # test HTTP reachability
docker network ls && docker network inspect <network>  # inspect network config
```

Services reach each other by **service name**, not `localhost`.
<!-- cs: Služby se dosahují přes jméno service, ne přes localhost. -->

## Step 3 — Quick fixes reference

<!-- cs: Krok 3 — Přehled rychlých oprav -->

| Problem | Fix |
|---------|-----|
| Stale image after code change | `docker compose build <svc>` |
| Stale image after dep change | `docker compose build --no-cache <svc>` |
| DB data corruption | `docker compose down -v` (⚠ deletes volumes) |
| Out of disk space | `docker system prune -f && docker volume prune -f` |
| Wrong env values | Check `.env`, verify with `docker compose config` |

<!-- cs: ⚠ docker compose down -v smaže volumes (data) — buď opatrný! -->

## Additional resources

- [04-docker-standards.mdc](../../rules/04-docker-standards.mdc) — Dockerfile and compose standards
