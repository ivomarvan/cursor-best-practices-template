#!/usr/bin/env bash
# Spusť tento skript po git clone pro aktivaci šifrování.
# Vyžaduje: age, gzip. Viz .veil/README_VEIL.md.
# Použití: bash .veil/setup_veil.sh <cesta_k_privatnimu_klici>
set -euo pipefail
KEY_PATH="${1:?Usage: bash $0 <path_to_private_key>}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${REPO_ROOT}"
git config filter.veil.clean "gzip -9 | age -r age1jugsr8nxkwsa7y0z42n9p25mq88aeln5cvumaqtalpn2vzds2fvsut6nf0"
git config filter.veil.smudge "age --decrypt -i ${KEY_PATH} | gzip -d"
git config filter.veil.required true
git config diff.veil.textconv "age --decrypt -i ${KEY_PATH} | gzip -d"
echo "veilgit filtry aktivovány."
