---
run_id: 20260817-1853-slice-and-derived-truth-66
intent_ids: ["i0004"]
role: Coder
model: cursor-grok-4.5-high
complexity: high
status: done
---

# Failing-test evidence

Všechny výstupy níže jsou přeměřené nad **finálním** working tree (fixtura s
`far_caller`, po round 3). Příkaz:
`python3 -m unittest discover -s tools/intent/tests -t tools`.
Po každé reverzi: `Ran 82 tests … OK`. `tools/intent/slicing.py` zůstává byte-identický
s `HEAD`.

Finální id ve fixtuře `c6` (12 uzlů):

| id | role |
|---|---|
| i0001 | root |
| i0002 | mid |
| i0003 | deeper_shared (outside) |
| i0004 | shared |
| i0005 | further_listener (outside) |
| i0006 | listener |
| i0007 | target |
| i0008 | caller |
| i0009 | far_caller (outside) |
| i0010 | sibling (outside) |
| i0011 | consumer (outside) |
| i0012 | child (outside) |

Kde test používá `subTest(for_implementation=…)`, unittest může nahlásit `failures=2`
pro **jednu** metodu. Jiná testová metoda nepadá.

---

## Mutace 1 — `c6`, příchozí hrana nese soubor

`tools/intent/slicing.py:80`

```diff
-     node_ids = [*ancestors, node_id, *result.uses, *result.talks_to]
+     node_ids = [*ancestors, node_id, *result.uses, *node.talks_to]
```

```
FAIL: test_slice_carries_exactly_ancestors_uses_and_talks_to_ends (...) (for_implementation=False)
FAIL: test_slice_carries_exactly_ancestors_uses_and_talks_to_ends (...) (for_implementation=True)
  File ".../test_tools.py", line 51, in test_slice_carries_exactly_ancestors_uses_and_talks_to_ends
    self.assertEqual(carried, expected)
AssertionError: Items in the second set but not the first:
'i0008'

Ran 82 tests in 0.179s
FAILED (failures=2)
```

Padla právě `test_slice_carries_exactly_…` (caller = `i0008`).
`test_slice_includes_incoming_talks_to` zůstal zelený.

---

## Mutace 2 — `c6`, příbuznost sama nepřidává

`tools/intent/slicing.py:80`

```diff
-     node_ids = [*ancestors, node_id, *result.uses, *result.talks_to]
+     siblings = [n.id for n in tree.nodes.values() if n.parent == node.parent and n.id != node_id]
+     node_ids = [*ancestors, node_id, *result.uses, *result.talks_to, *siblings]
```

```
FAIL: test_slice_carries_exactly_ancestors_uses_and_talks_to_ends (...) (for_implementation=False)
FAIL: test_slice_carries_exactly_ancestors_uses_and_talks_to_ends (...) (for_implementation=True)
  File ".../test_tools.py", line 51, in test_slice_carries_exactly_ancestors_uses_and_talks_to_ends
    self.assertEqual(carried, expected)
AssertionError: Items in the first set but not the second:
'i0010'

Ran 82 tests in 0.181s
FAILED (failures=2)
```

Padla právě `test_slice_carries_exactly_…` (sibling pod `mid` = `i0010`).

---

## Mutace 3 — `c7`, druhé místo odvození

`tools/intent/generate.py:92`

```diff
-             reverse.append({"code_path": code_path, "node": node.id, "depth": str(len(path) - 1)})
+             reverse.append({"code_path": code_path, "node": node.id, "depth": "0"})
```

```
FAIL: test_index_holds_derived_path_and_depth (...)
  File ".../test_tools.py", line 173, in test_index_holds_derived_path_and_depth
    self.assertEqual(str(row["depth"]), "2")
AssertionError: '0' != '2'

Ran 82 tests in 0.168s
FAILED (failures=1)
```

Padl právě jeden test. `test_reverse_lookup_prefers_the_deepest_node` zelený.

---

## Mutace 4 — `c19`, dosah na `_retired/`

`tools/intent/validate.py:62` — první cyklus `tree.retired` → `tree.nodes`.

```diff
-     for node in tree.retired.values():
+     for node in tree.nodes.values():
```

```
FAIL: test_derived_fields_in_a_node_file_are_reported (...)
  File ".../test_validate.py", line 199, in test_derived_fields_in_a_node_file_are_reported
    self.assertIn(gone, flagged_path)
AssertionError: 'i0006' not found in {'i0002', 'i0003'}

Ran 82 tests in 0.184s
FAILED (failures=1)
```

Padl právě jeden test (`gone` = `i0006`; `i0002`/`i0003` = engine / path_only).

---

## Mutace 5 — B1 (a): jen rodič, ne řetězec předků

`tools/intent/slicing.py:69`

```diff
-     ancestors = [item.id for item in tree.ancestors(node_id)]
+     ancestors = [item.id for item in tree.ancestors(node_id)][-1:]
```

```
FAIL: test_slice_carries_exactly_ancestors_uses_and_talks_to_ends (...) (for_implementation=False)
FAIL: test_slice_carries_exactly_ancestors_uses_and_talks_to_ends (...) (for_implementation=True)
  File ".../test_tools.py", line 51, in test_slice_carries_exactly_ancestors_uses_and_talks_to_ends
    self.assertEqual(carried, expected)
AssertionError: Items in the second set but not the first:
'i0001'

Ran 82 tests in 0.172s
FAILED (failures=2)
```

Padla právě `test_slice_carries_exactly_…` (chybí root = `i0001`).

---

## Mutace 6 — B1 (b): tranzitivní `uses`

`tools/intent/slicing.py:76`

```diff
-         uses=sorted(node.uses),
+         uses=sorted(set(node.uses) | {u for t in node.uses if t in tree.nodes for u in tree.nodes[t].uses}),
```

```
FAIL: test_slice_carries_exactly_ancestors_uses_and_talks_to_ends (...) (for_implementation=False)
FAIL: test_slice_carries_exactly_ancestors_uses_and_talks_to_ends (...) (for_implementation=True)
  File ".../test_tools.py", line 51, in test_slice_carries_exactly_ancestors_uses_and_talks_to_ends
    self.assertEqual(carried, expected)
AssertionError: Items in the first set but not the second:
'i0003'

Ran 82 tests in 0.169s
FAILED (failures=2)
```

Padla právě `test_slice_carries_exactly_…` (`deeper_shared` = `i0003`).

---

## Mutace 7 — B1 (c): dva skoky `talks_to` (vlastní hrana)

`tools/intent/slicing.py:71`

```diff
-     talks = sorted(set(node.talks_to) | set(incoming))
+     talks = set(node.talks_to) | set(incoming)
+     talks = sorted(talks | {t for m in list(talks) if m in tree.nodes for t in tree.nodes[m].talks_to})
```

```
FAIL: test_slice_carries_exactly_ancestors_uses_and_talks_to_ends (...) (for_implementation=False)
FAIL: test_slice_carries_exactly_ancestors_uses_and_talks_to_ends (...) (for_implementation=True)
  File ".../test_tools.py", line 51, in test_slice_carries_exactly_ancestors_uses_and_talks_to_ends
    self.assertEqual(carried, expected)
AssertionError: Items in the first set but not the second:
'i0005'

Ran 82 tests in 0.175s
FAILED (failures=2)
```

Padla právě `test_slice_carries_exactly_…` (`further_listener` = `i0005`).

---

## Mutace 8 — B2: potomci při `for_implementation=True`

`tools/intent/slicing.py:80`

```diff
     node_ids = [*ancestors, node_id, *result.uses, *result.talks_to]
+    if for_implementation:
+        node_ids += [child.id for child in tree.children_of(node_id)]
```

```
FAIL: test_slice_carries_exactly_ancestors_uses_and_talks_to_ends (...) (for_implementation=True)
  File ".../test_tools.py", line 51, in test_slice_carries_exactly_ancestors_uses_and_talks_to_ends
    self.assertEqual(carried, expected)
AssertionError: Items in the first set but not the second:
'i0012'

Ran 82 tests in 0.168s
FAILED (failures=1)
```

Padla právě `test_slice_carries_exactly_…`, jen větev `True` (`child` = `i0012`).
`test_slice_lists_owned_code_when_implementing` zelený.

---

## Mutace 9 — B3: `path or depth` vyžaduje obě pole

`tools/intent/validate.py:54`

```diff
-     if node.unknown_fields:
+     if len(node.unknown_fields) > 1:
```

```
FAIL: test_derived_fields_in_a_node_file_are_reported (...)
  File ".../test_validate.py", line 193, in test_derived_fields_in_a_node_file_are_reported
    self.assertIn(path_only, flagged_path)
AssertionError: 'i0003' not found in {'i0002', 'i0006'}

Ran 82 tests in 0.173s
FAILED (failures=1)
```

Padl právě jeden test (`path_only` = `i0003`; `i0002`/`i0006` = engine/gone).

---

## Mutace 10 — B4: příchozí `talks_to` jen jeden hop

`tools/intent/slicing.py:70`

```diff
-     incoming = sorted(other.id for other in tree.nodes.values() if node_id in other.talks_to)
+     first = {other.id for other in tree.nodes.values() if node_id in other.talks_to}
+     second = {o.id for o in tree.nodes.values() if any(f in o.talks_to for f in first)}
+     incoming = sorted(first | second)
```

```
FAIL: test_slice_carries_exactly_ancestors_uses_and_talks_to_ends (...) (for_implementation=False)
FAIL: test_slice_carries_exactly_ancestors_uses_and_talks_to_ends (...) (for_implementation=True)
  File ".../test_tools.py", line 51, in test_slice_carries_exactly_ancestors_uses_and_talks_to_ends
    self.assertEqual(carried, expected)
AssertionError: Items in the first set but not the second:
'i0009'

Ran 82 tests in 0.170s
FAILED (failures=2)
```

Padla právě `test_slice_carries_exactly_…` (`far_caller` = `i0009`).

---

## Shrnutí (finální fixtura)

| # | Co | Uniklý / chybějící id | Aserce | Failures |
|---|---|---|---|---|
| 1 | `*node.talks_to` | chybí `i0008` (caller) | `test_tools.py:51` | 2 (subTest) |
| 2 | sourozenci | unikl `i0010` (sibling) | `:51` | 2 |
| 3 | reverse depth `"0"` | `'0' != '2'` | `test_tools.py:173` | 1 |
| 4 | retired → nodes | chybí `i0006` (gone) | `test_validate.py:199` | 1 |
| 5 | `ancestors[-1:]` | chybí `i0001` (root) | `:51` | 2 |
| 6 | tranzitivní uses | unikl `i0003` (deeper_shared) | `:51` | 2 |
| 7 | dva skoky vlastní talks_to | unikl `i0005` (further_listener) | `:51` | 2 |
| 8 | potomci při implement | unikl `i0012` (child), jen True | `:51` | 1 |
| 9 | `len(unknown) > 1` | chybí `i0003` (path_only) | `test_validate.py:193` | 1 |
| 10 | dva skoky incoming | unikl `i0009` (far_caller) | `:51` | 2 |
