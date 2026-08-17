---
run_id: 20260816-2145-contract-hygiene-cd
intent_ids: ["i0004"]
role: Grader
model: none — the Grader is not a language model
complexity: high
status: in-progress
---

# Grader log

## Failing-test evidence — one mutation per assertion

Each mutation was applied, the suite run, the output captured, then reverted. All four
mutations reproduce exactly what `plan.md` predicted: each fails the one test it targets
and nothing else.

### Mutation 1 — `c4` — cousins half of `test_overlap_outside_the_ancestor_chain_is_rejected`

`_check_code_paths` reports `V6` only for pairs that share a common parent (siblings),
instead of for any pair outside the ancestor chain.

```diff
--- a/tools/intent/validate.py
+++ b/tools/intent/validate.py
@@ def _check_code_paths(tree: Tree, out: _Collector) -> None:
-            if _is_ancestor(tree, node_a, node_b) or _is_ancestor(tree, node_b, node_a):
-                continue
+            if tree.nodes[node_a].parent != tree.nodes[node_b].parent:
+                continue
             out.error(
                 "V6",
```

```
$ python3 -m unittest discover -s tools/intent/tests -t tools
................................................................F.................
======================================================================
FAIL: test_overlap_outside_the_ancestor_chain_is_rejected (intent.tests.test_validate.CodePathTest.test_overlap_outside_the_ancestor_chain_is_rejected)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/ivo/workspace/git.hub.lab.ivo/cursor-best-practices-template/tools/intent/tests/test_validate.py", line 165, in test_overlap_outside_the_ancestor_chain_is_rejected
    self.assertTrue({cousin_a, cousin_b} & flagged)
    ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: set() is not true

----------------------------------------------------------------------
Ran 82 tests in 0.286s

FAILED (failures=1)
```

exit code: 1

Reverted; suite green again:

```
$ python3 -m unittest discover -s tools/intent/tests -t tools
..................................................................................
----------------------------------------------------------------------
Ran 82 tests in 0.255s

OK
```

exit code: 0

### Mutation 2 — `c18` — grandparent–grandchild half of `test_the_ancestor_chain_may_overlap`

`_is_ancestor` compares only the direct parent instead of walking the whole ancestor
chain.

```diff
--- a/tools/intent/validate.py
+++ b/tools/intent/validate.py
@@
-def _is_ancestor(tree: Tree, ancestor_id: str, node_id: str) -> bool:
-    return ancestor_id in [node.id for node in tree.ancestors(node_id)]
+def _is_ancestor(tree: Tree, ancestor_id: str, node_id: str) -> bool:
+    node = tree.nodes.get(node_id)
+    return node is not None and node.parent == ancestor_id
```

```
$ python3 -m unittest discover -s tools/intent/tests -t tools
.................................................................F................
======================================================================
FAIL: test_the_ancestor_chain_may_overlap (intent.tests.test_validate.CodePathTest.test_the_ancestor_chain_may_overlap)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/ivo/workspace/git.hub.lab.ivo/cursor-best-practices-template/tools/intent/tests/test_validate.py", line 143, in test_the_ancestor_chain_may_overlap
    self.assertNotIn("V6", self.codes(tree))
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'V6' unexpectedly found in ['V6']

----------------------------------------------------------------------
Ran 82 tests in 0.271s

FAILED (failures=1)
```

exit code: 1

Reverted; suite green again:

```
$ python3 -m unittest discover -s tools/intent/tests -t tools
..................................................................................
----------------------------------------------------------------------
Ran 82 tests in 0.228s

OK
```

exit code: 0

### Mutation 3 — `c19` — `test_derived_fields_in_a_node_file_are_reported`

`path` and `depth` are added to `KNOWN_FIELDS`, so they stop being reported as unknown
fields.

```diff
--- a/tools/intent/model.py
+++ b/tools/intent/model.py
@@
 KNOWN_FIELDS = {
     "id",
     "parent",
     "slug",
     "title",
     "status",
     "superseded_by",
     "contracts",
+    "path",
+    "depth",
     *LIST_FIELDS,
 }
```

```
$ python3 -m unittest discover -s tools/intent/tests -t tools
.......................................................................F..........
======================================================================
FAIL: test_derived_fields_in_a_node_file_are_reported (intent.tests.test_validate.DerivedFieldTest.test_derived_fields_in_a_node_file_are_reported)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/ivo/workspace/git.hub.lab.ivo/cursor-best-practices-template/tools/intent/tests/test_validate.py", line 179, in test_derived_fields_in_a_node_file_are_reported
    self.assertIn(engine, flagged)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
AssertionError: 'i0002' not found in set()

----------------------------------------------------------------------
Ran 82 tests in 0.389s

FAILED (failures=1)
```

exit code: 1

Reverted; suite green again:

```
$ python3 -m unittest discover -s tools/intent/tests -t tools
..................................................................................
----------------------------------------------------------------------
Ran 82 tests in 0.269s

OK
```

exit code: 0

### Mutation 4 — `c20` — `test_a_path_in_a_node_file_does_not_reach_the_index`

`Node` gains a `written_path` field populated straight from front matter, and
`build_index` prefers it over the computed ancestor-chain path.

```diff
--- a/tools/intent/model.py
+++ b/tools/intent/model.py
@@ class Node:
     unknown_fields: list[str] = field(default_factory=list)
     retired_file: bool = False
+    written_path: str | None = None
@@ def parse_node(path: Path) -> Node:
         unknown_fields=sorted(set(data) - KNOWN_FIELDS),
         retired_file=path.parent.name == RETIRED_DIRNAME,
+        written_path=None if data.get("path") is None else str(data.get("path")),
     )
--- a/tools/intent/generate.py
+++ b/tools/intent/generate.py
@@ def build_index(tree: Tree) -> dict[str, object]:
             "parent": node.parent,
-            "path": "/".join(path),
+            "path": node.written_path or "/".join(path),
```

```
$ python3 -m unittest discover -s tools/intent/tests -t tools
....................................................F..............................
======================================================================
FAIL: test_a_path_in_a_node_file_does_not_reach_the_index (intent.tests.test_tools.GeneratedViewTest.test_a_path_in_a_node_file_does_not_reach_the_index)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/ivo/workspace/git.hub.lab.ivo/cursor-best-practices-template/tools/intent/tests/test_tools.py", line 151, in test_a_path_in_a_node_file_does_not_reach_the_index
    self.assertEqual(index["nodes"][child]["path"], f"{root}/{child}")
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'nonsense/place' != 'i0001/i0002'
- nonsense/place
+ i0001/i0002


----------------------------------------------------------------------
Ran 82 tests in 0.282s

FAILED (failures=1)
```

exit code: 1

Reverted; suite green again:

```
$ python3 -m unittest discover -s tools/intent/tests -t tools
..................................................................................
----------------------------------------------------------------------
Ran 82 tests in 0.233s

OK
```

exit code: 0

Working tree after all four reverts (`validate.py`, `model.py`, `generate.py`): no diff against
HEAD, confirmed with `git diff --stat`.

## VERIFY.md mandate

```
$ python3 tools/intent/cli.py validate

5 node(s): 0 error(s), 0 warning(s)
```

exit code: 0

```
$ python3 tools/intent/cli.py realization check
realization layer consistent (1 entry/entries)
```

exit code: 0

Note: `intent realization status --node i0004` reports `i0004  stale [own contracts
changed; own meaning changed]`, as the plan and the run instructions expect. This is not
fixed and no claim is written — that is the Coordinator's job after this log is green.

```
$ python3 -m unittest discover -s tools/intent/tests -t tools
..................................................................................
----------------------------------------------------------------------
Ran 82 tests in 0.218s

OK
```

exit code: 0

```
$ python3 tools/checks/template_checks.py --root .
template contracts satisfied
```

exit code: 0

```
$ python3 tools/checks/hook_checks.py --root .
hook contracts satisfied
```

exit code: 0

```
$ python3 tools/intent/cli.py scope --run doc/runs/20260816-2145-contract-hygiene-cd
scope clean (6 declared path(s))
```

exit code: 0

## Coder self-check (outside the VERIFY.md mandate)

```
$ ruff check tools/
All checks passed!
```

exit code: 0

```
$ ruff format --check tools/
19 files already formatted
```

exit code: 0
