---
run_id: 20260817-1703-views-hygiene-dc
intent_ids: ["i0004"]
role: Grader
model: none — the Grader is not a language model
complexity: high
status: in-progress
---

# Grader log

## Failing-test evidence

### Mutation 1 — `path` on `Node` + prefer in `build_index`

Expected: index half of `test_a_path_in_a_node_file_does_not_reach_a_generated_view` fails.
Production files reverted after capture.

#### Diff `tools/intent/model.py`
```
--- /tmp/model.py.bak	2026-08-17 17:13:50.857530478 +0200
+++ tools/intent/model.py	2026-08-17 17:13:50.986531597 +0200
@@ -68,6 +68,7 @@
     source: Path | None = None
     unknown_fields: list[str] = field(default_factory=list)
     retired_file: bool = False
+    path: str | None = None  # MUTATION: accept path from front matter
 
     @property
     def body_line_count(self) -> int:
@@ -145,6 +146,7 @@
         source=path,
         unknown_fields=sorted(set(data) - KNOWN_FIELDS),
         retired_file=path.parent.name == RETIRED_DIRNAME,
+        path=None if data.get("path") is None else str(data.get("path")),
     )
 
 
```
#### Diff `tools/intent/generate.py`
```
--- /tmp/generate.py.bak	2026-08-17 17:13:50.865530547 +0200
+++ tools/intent/generate.py	2026-08-17 17:13:50.987531606 +0200
@@ -69,7 +69,7 @@
             "title": node.title,
             "status": node.status,
             "parent": node.parent,
-            "path": "/".join(path),
+            "path": node.path if node.path is not None else "/".join(path),
             "depth": len(path) - 1,
             "children": [child.id for child in tree.children_of(node.id)],
             "uses": node.uses,
```
#### Suite output
```
....................................................F.............................
======================================================================
FAIL: test_a_path_in_a_node_file_does_not_reach_a_generated_view (intent.tests.test_tools.GeneratedViewTest.test_a_path_in_a_node_file_does_not_reach_a_generated_view)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/ivo/workspace/git.hub.lab.ivo/cursor-best-practices-template/tools/intent/tests/test_tools.py", line 153, in test_a_path_in_a_node_file_does_not_reach_a_generated_view
    self.assertEqual(index["nodes"][child]["path"], expected_path)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'nonsense/place' != 'i0001/i0002'
- nonsense/place
+ i0001/i0002


----------------------------------------------------------------------
Ran 82 tests in 0.548s

FAILED (failures=1)
```
exit code: 1

### Mutation 2 — `path` on `Node` + prefer in `render_map`

Expected: map half fails (index half stays green). Production files reverted after capture.

#### Diff `tools/intent/model.py`
```
--- /tmp/model.py.bak	2026-08-17 17:13:50.857530478 +0200
+++ tools/intent/model.py	2026-08-17 17:13:52.128541511 +0200
@@ -68,6 +68,7 @@
     source: Path | None = None
     unknown_fields: list[str] = field(default_factory=list)
     retired_file: bool = False
+    path: str | None = None  # MUTATION: accept path from front matter
 
     @property
     def body_line_count(self) -> int:
@@ -145,6 +146,7 @@
         source=path,
         unknown_fields=sorted(set(data) - KNOWN_FIELDS),
         retired_file=path.parent.name == RETIRED_DIRNAME,
+        path=None if data.get("path") is None else str(data.get("path")),
     )
 
 
```
#### Diff `tools/intent/generate.py`
```
--- /tmp/generate.py.bak	2026-08-17 17:13:50.865530547 +0200
+++ tools/intent/generate.py	2026-08-17 17:13:52.129541520 +0200
@@ -31,7 +31,7 @@
         "|----|------|-------|-----------|------|",
     ]
     for node in tree.sorted_nodes():
-        path = "/".join(tree.path_of(node.id))
+        path = node.path if node.path is not None else "/".join(tree.path_of(node.id))
         code = ", ".join(f"`{item}`" for item in node.code_paths) or "—"
         contracts = _contract_summary(tree, node.id).replace("|", "\\|")
         title = node.title.replace("|", "\\|")
```
#### Suite output
```
....................................................F.............................
======================================================================
FAIL: test_a_path_in_a_node_file_does_not_reach_a_generated_view (intent.tests.test_tools.GeneratedViewTest.test_a_path_in_a_node_file_does_not_reach_a_generated_view)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/ivo/workspace/git.hub.lab.ivo/cursor-best-practices-template/tools/intent/tests/test_tools.py", line 163, in test_a_path_in_a_node_file_does_not_reach_a_generated_view
    self.assertIn(f"`{expected_path}`", row)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: '`i0001/i0002`' not found in '| `i0002` | `nonsense/place` | engine | — | — |'

----------------------------------------------------------------------
Ran 82 tests in 0.269s

FAILED (failures=1)
```
exit code: 1

### Green after revert

Both mutations reverted; production `model.py` / `generate.py` unchanged.
```
..................................................................................
----------------------------------------------------------------------
Ran 82 tests in 0.243s

OK
```
exit code: 0

## Gates (`VERIFY.md`)

### `python3 tools/intent/cli.py validate`
```

5 node(s): 0 error(s), 0 warning(s)
```
exit code: 0

### `python3 tools/intent/cli.py realization check`
```
realization layer consistent (1 entry/entries)
```
exit code: 0

Note: `i0004` remains `stale` (expected). No realization claim written by the Coder.

### `python3 -m unittest discover -s tools/intent/tests -t tools`
```
..................................................................................
----------------------------------------------------------------------
Ran 82 tests in 0.243s

OK
```
exit code: 0

### `python3 tools/checks/template_checks.py --root .`
```
template contracts satisfied
```
exit code: 0

### `python3 tools/checks/hook_checks.py --root .`
```
hook contracts satisfied
```
exit code: 0

### `python3 tools/intent/cli.py scope --run doc/runs/20260817-1703-views-hygiene-dc`
```
scope clean (6 declared path(s))
```
exit code: 0

## Coder self-check (outside `VERIFY.md` mandate)

### `ruff check tools/`
```
All checks passed!
```
exit code: 0

### `ruff format --check tools/`
```
19 files already formatted
```
exit code: 0


---

# Round 2 — Adversary REQUEST CHANGES

Append-only. Earlier captures above are unchanged.

## Failing-test evidence

### Mutation 3 — `path` on `Node` + leak into mermaid label in `render_map`

Expected: document-wide `assertNotIn("nonsense/place", text)` fails; row assertions stay green.
Production files reverted after capture.

#### Diff `tools/intent/model.py`
```
--- /tmp/model.py.bak	2026-08-17 17:26:49.486314991 +0200
+++ tools/intent/model.py	2026-08-17 17:26:50.296322082 +0200
@@ -68,6 +68,7 @@
     source: Path | None = None
     unknown_fields: list[str] = field(default_factory=list)
     retired_file: bool = False
+    path: str | None = None  # MUTATION: accept path from front matter
 
     @property
     def body_line_count(self) -> int:
@@ -145,6 +146,7 @@
         source=path,
         unknown_fields=sorted(set(data) - KNOWN_FIELDS),
         retired_file=path.parent.name == RETIRED_DIRNAME,
+        path=None if data.get("path") is None else str(data.get("path")),
     )
```
#### Diff `tools/intent/generate.py`
```
--- /tmp/generate.py.bak	2026-08-17 17:26:49.494315061 +0200
+++ tools/intent/generate.py	2026-08-17 17:26:50.297322091 +0200
@@ -42,7 +42,10 @@
     lines.append("```mermaid")
     lines.append("graph TD")
     for node in tree.sorted_nodes():
-        label = f"{node.id}<br/>{node.title}".replace('"', "'")
+        label = f"{node.id}<br/>{node.title}"
+        if node.path is not None:
+            label = f"{label}<br/>{node.path}"
+        label = label.replace('"', "'")
         lines.append(f'    {node.id}["{label}"]')
     for node in tree.sorted_nodes():
         if node.parent:
```
#### Suite output
```
....................................................F.............................
======================================================================
FAIL: test_a_path_in_a_node_file_does_not_reach_a_generated_view (intent.tests.test_tools.GeneratedViewTest.test_a_path_in_a_node_file_does_not_reach_a_generated_view)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/ivo/workspace/git.hub.lab.ivo/cursor-best-practices-template/tools/intent/tests/test_tools.py", line 169, in test_a_path_in_a_node_file_does_not_reach_a_generated_view
    self.assertNotIn("nonsense/place", text)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'nonsense/place' unexpectedly found in '# Intent map\n\n<!-- generated by `intent map` — do not edit by hand -->\n\n| Id | Path | Title | Contracts | Code |\n|----|------|-------|-----------|------|\n| `i0001` | `i0001` | system | — | — |\n| `i0002` | `i0001/i0002` | engine | — | — |\n\n## Tree\n\n```mermaid\ngraph TD\n    i0001["i0001<br/>system"]\n    i0002["i0002<br/>engine<br/>nonsense/place"]\n    i0001 --> i0002\n```\n'

----------------------------------------------------------------------
Ran 82 tests in 1.087s

FAILED (failures=1)
```
exit code: 1

### Green after revert (round 2)

Both production files reverted; suite green with the document-wide assertion present.
```
..................................................................................
----------------------------------------------------------------------
Ran 82 tests in 1.214s

OK
```
exit code: 0

## Gates re-run (round 2)

### `python3 tools/intent/cli.py validate`
```

5 node(s): 0 error(s), 0 warning(s)
```
exit code: 0

### `python3 tools/intent/cli.py realization check`
```
realization layer consistent (1 entry/entries)
```
exit code: 0

### `python3 -m unittest discover -s tools/intent/tests -t tools`
```
..................................................................................
----------------------------------------------------------------------
Ran 82 tests in 1.214s

OK
```
exit code: 0

### `python3 tools/checks/template_checks.py --root .`
```
template contracts satisfied
```
exit code: 0

### `python3 tools/checks/hook_checks.py --root .`
```
hook contracts satisfied
```
exit code: 0

### `python3 tools/intent/cli.py scope --run doc/runs/20260817-1703-views-hygiene-dc`
```
scope clean (6 declared path(s))
```
exit code: 0

## Coder self-check (round 2, outside `VERIFY.md` mandate)

### `ruff check tools/`
```
All checks passed!
```
exit code: 0

### `ruff format --check tools/`
```
19 files already formatted
```
exit code: 0


---

# Round 3 — comment wording (APPROVE follow-up)

Append-only. Earlier captures above are unchanged. Comment-only change in
`test_a_path_in_a_node_file_does_not_reach_a_generated_view`: ordering explained without
referring to a run, mutation or grader.

## Gates re-run (round 3)

### `python3 tools/intent/cli.py validate`
```

5 node(s): 0 error(s), 0 warning(s)
```
exit code: 0

### `python3 tools/intent/cli.py realization check`
```
realization layer consistent (1 entry/entries)
```
exit code: 0

### `python3 -m unittest discover -s tools/intent/tests -t tools`
```
..................................................................................
----------------------------------------------------------------------
Ran 82 tests in 0.290s

OK
```
exit code: 0

### `python3 tools/checks/template_checks.py --root .`
```
template contracts satisfied
```
exit code: 0

### `python3 tools/checks/hook_checks.py --root .`
```
hook contracts satisfied
```
exit code: 0

### `python3 tools/intent/cli.py scope --run doc/runs/20260817-1703-views-hygiene-dc`
```
scope clean (6 declared path(s))
```
exit code: 0

## Coder self-check (round 3, outside `VERIFY.md` mandate)

### `ruff check tools/`
```
All checks passed!
```
exit code: 0

### `ruff format --check tools/`
```
19 files already formatted
```
exit code: 0
