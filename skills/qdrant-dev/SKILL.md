---
name: qdrant-dev
description: >-
  Qdrant vector database development workflow in Docker. Use when working with
  Qdrant collections, point upsert, vector search, payload indexing, or debugging
  Qdrant-related issues. Covers: starting the container, inspecting collections,
  running Python scripts against Qdrant, and backup/restore.
---

# Qdrant Dev Workflow (Docker)

<!-- cs: Vývojový workflow pro Qdrant přes Docker -->

## Prerequisites

<!-- cs: Předpoklady -->

- `docker compose up qdrant` running (port 6333 REST, 6334 gRPC).
- Python environment with `qdrant-client[grpc]` installed.

<!-- cs: Docker compose s Qdrant běží; Python prostředí s qdrant-client[grpc]. -->

## 1. Start / Stop Qdrant

<!-- cs: Spuštění / zastavení Qdrant -->

```bash
# start (detached)
docker compose up -d qdrant

# check logs
docker compose logs -f qdrant

# stop
docker compose stop qdrant
```

**Health check:**
<!-- cs: Kontrola dostupnosti: -->

```bash
curl -s http://localhost:6333/healthz
# expected: {"title":"qdrant - vector search engine","version":"..."}

curl -s http://localhost:6333/collections | python3 -m json.tool
```

## 2. Inspect Collections

<!-- cs: Prohlížení kolekcí -->

```bash
# List all collections
curl -s http://localhost:6333/collections | python3 -m json.tool

# Collection info (config, vector count, index status)
curl -s http://localhost:6333/collections/documents | python3 -m json.tool

# Count points
curl -s http://localhost:6333/collections/documents/points/count | python3 -m json.tool
```

## 3. Run Python Scripts Against Qdrant

<!-- cs: Spuštění Python skriptů vůči Qdrant -->

```bash
# Run indexing / migration script from host (Qdrant reachable at localhost:6333)
docker compose exec app python src/indexing/build_index.py

# Or run script directly on host if Python environment is local
python src/indexing/build_index.py

# Interactive Python shell for ad-hoc queries
docker compose exec app python
```

```python
# Quick connectivity test
from qdrant_client import QdrantClient
client = QdrantClient(url="http://localhost:6333")
print(client.get_collections())
```

## 4. Collection Management

<!-- cs: Správa kolekcí -->

```bash
# Delete a collection (destructive — data loss)
curl -X DELETE http://localhost:6333/collections/documents

# Recreate / reindex — run the collection setup script
docker compose exec app python src/db/create_collections.py
```

```python
# In-memory client for unit tests — no Docker needed
from qdrant_client import AsyncQdrantClient
client = AsyncQdrantClient(":memory:")
```

## 5. Search Test (ad-hoc)

<!-- cs: Testovací dotaz -->

```bash
# Nearest neighbour search via REST — replace vectors with real floats
curl -X POST http://localhost:6333/collections/documents/points/search \
  -H 'Content-Type: application/json' \
  -d '{
    "vector": [0.1, 0.2, ...],
    "limit": 5,
    "with_payload": true
  }' | python3 -m json.tool
```

## 6. Backup and Restore

<!-- cs: Záloha a obnova -->

```bash
# Create snapshot (stored inside the container volume)
curl -X POST http://localhost:6333/collections/documents/snapshots

# List snapshots
curl http://localhost:6333/collections/documents/snapshots | python3 -m json.tool

# Download snapshot to host
SNAPSHOT_NAME=$(curl -s http://localhost:6333/collections/documents/snapshots \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['result'][-1]['name'])")
curl -o "backup_${SNAPSHOT_NAME}.snapshot" \
  "http://localhost:6333/collections/documents/snapshots/${SNAPSHOT_NAME}"

# Restore from snapshot (collection must not exist)
curl -X POST "http://localhost:6333/collections/documents/snapshots/recover" \
  -H 'Content-Type: application/json' \
  -d "{\"location\": \"file:///qdrant/storage/collections/documents/snapshots/${SNAPSHOT_NAME}\"}"
```

## 7. Cleanup

<!-- cs: Cleanup -->

```bash
# Remove container + volume (destroys all vector data)
docker compose down -v qdrant

# Remove only unused volumes (keep named ones)
docker volume prune -f
```
