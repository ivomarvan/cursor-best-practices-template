#!/usr/bin/env python3
"""Launcher so the tool can be run straight from a checkout or a submodule.

python3 .cursor/tools/intent/cli.py validate
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from intent.main import main

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
