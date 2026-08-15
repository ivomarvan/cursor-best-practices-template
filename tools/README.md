# Tools

Executable part of the harness. No third-party dependencies: these scripts must run
before a project has an environment, and inside a submodule where installing packages
would be someone else's decision. Python 3.11 or newer.

```
tools/
├── intent/            # the intent tree: validation, ids, views, slices, guards
│   ├── cli.py         # entry point
│   ├── miniyaml.py    # the restricted YAML subset used by node front matter
│   ├── model.py       # nodes, registry, derived structure
│   ├── validate.py    # machine rules V1-V10
│   ├── generate.py    # MAP.md and INDEX.json
│   ├── slicing.py     # context slice
│   ├── scope.py       # scope guard
│   ├── coverage.py    # contracts without enforcers, code without nodes
│   └── tests/         # unittest, no pytest needed
└── checks/            # contracts this repository declares about itself
    ├── template_checks.py
    └── hook_checks.py
```

## Usage

```bash
# inside this repository
python3 tools/intent/cli.py --help

# in a project where the harness is mounted at .cursor/
python3 .cursor/tools/intent/cli.py --help
```

| Command | Purpose |
|---------|---------|
| `validate` | machine rules V1–V10; exit 1 on error, 0 with warnings only |
| `map` | regenerate `MAP.md` and `INDEX.json` |
| `new --parent iNNNN --slug x [--title T]` | allocate an id and scaffold a node |
| `move iNNNN --parent iMMMM` | re-parent a node without changing its id |
| `slice iNNNN --for plan\|implement` | the file list for one agent action |
| `scope --run <dir> [--base <ref>] [--node iNNNN]` | diff versus declared outputs |
| `coverage [--strict]` | contracts without a machine enforcer, code outside any node |
| `owner <path>` | which node governs a file (deepest node wins) |

`--root <dir>` overrides the project root. Without it, the tool walks up from the current
directory to the nearest ancestor containing `doc/intent/`.

## Where the tool looks

Only at `doc/intent/` in the **project root**. `.cursor/` is ignored unconditionally: a
harness mounted as a submodule carries its own intent tree, and two registries in one
project would make every short id ambiguous.

## Tests

```bash
python3 -m unittest discover -s tools/intent/tests -t tools
```

`-t tools` sets the top-level import directory so the test modules resolve as
`intent.tests.*`.
