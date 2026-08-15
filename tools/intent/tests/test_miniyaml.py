"""Tests for the restricted YAML subset."""

import unittest

from intent.miniyaml import YamlError, dump, parse, split_front_matter, strip_comment


class ParseScalarTest(unittest.TestCase):
    def test_scalars_and_types(self):
        data = parse(
            "\n".join(
                [
                    "id: i0042",
                    "count: 7",
                    "ratio: 1.5",
                    "flag: true",
                    "other: false",
                    "empty:",
                    "nothing: null",
                    'quoted: "a: b"',
                    "single: 'text'",
                ]
            )
        )
        self.assertEqual(data["id"], "i0042")
        self.assertEqual(data["count"], 7)
        self.assertEqual(data["ratio"], 1.5)
        self.assertIs(data["flag"], True)
        self.assertIs(data["other"], False)
        self.assertIsNone(data["empty"])
        self.assertIsNone(data["nothing"])
        self.assertEqual(data["quoted"], "a: b")
        self.assertEqual(data["single"], "text")

    def test_flow_sequences_and_mappings(self):
        data = parse("uses: [i0001, i0002]\nempty: []\ninline: {slug: system}")
        self.assertEqual(data["uses"], ["i0001", "i0002"])
        self.assertEqual(data["empty"], [])
        self.assertEqual(data["inline"], {"slug": "system"})

    def test_comment_stripping_respects_quotes(self):
        self.assertEqual(strip_comment('a: "x # y"  # tail'), 'a: "x # y"  ')
        data = parse('text: "hash # inside"  # comment')
        self.assertEqual(data["text"], "hash # inside")


class ParseBlockTest(unittest.TestCase):
    def test_nested_mapping(self):
        data = parse("issued:\n  i0001:\n    slug: system\n  i0002:\n    slug: engine\n")
        self.assertEqual(data["issued"]["i0001"]["slug"], "system")
        self.assertEqual(data["issued"]["i0002"]["slug"], "engine")

    def test_sequence_of_mappings(self):
        text = "\n".join(
            [
                "contracts:",
                "  - id: c1",
                "    text: user_id is unique",
                "    enforced_by: tests/test_db.py::test_unique",
                "  - id: c2",
                "    text: second",
                "    enforced_by: review",
                "    reason: needs a snapshot",
            ]
        )
        data = parse(text)
        self.assertEqual(len(data["contracts"]), 2)
        self.assertEqual(data["contracts"][0]["id"], "c1")
        self.assertEqual(data["contracts"][1]["reason"], "needs a snapshot")

    def test_sequence_of_scalars(self):
        data = parse("open_questions:\n  - first\n  - second\n")
        self.assertEqual(data["open_questions"], ["first", "second"])


class RejectionTest(unittest.TestCase):
    def test_anchor_is_rejected(self):
        with self.assertRaises(YamlError):
            parse("value: &anchor 1")

    def test_block_scalar_is_rejected(self):
        with self.assertRaises(YamlError):
            parse("text: |")

    def test_tabs_are_rejected(self):
        with self.assertRaises(YamlError):
            parse("root:\n\tchild: 1")

    def test_missing_front_matter(self):
        with self.assertRaises(YamlError):
            split_front_matter("# no front matter\n")

    def test_unterminated_front_matter(self):
        with self.assertRaises(YamlError):
            split_front_matter("---\nid: i0001\n")


class RoundTripTest(unittest.TestCase):
    def test_dump_then_parse(self):
        original = {
            "id": "i0042",
            "parent": None,
            "slug": "schema",
            "status": "current",
            "uses": ["i0019"],
            "empty": [],
            "contracts": [
                {"id": "c1", "text": "user_id is unique", "enforced_by": "tests/t.py::x"}
            ],
        }
        self.assertEqual(parse(dump(original)), original)

    def test_special_strings_are_quoted(self):
        original = {"text": "true", "other": "- leading dash", "third": "a: b"}
        self.assertEqual(parse(dump(original)), original)

    def test_split_front_matter(self):
        front, body = split_front_matter("---\nid: i0001\n---\n\n# Title\n")
        self.assertEqual(parse(front)["id"], "i0001")
        self.assertIn("# Title", body)


if __name__ == "__main__":
    unittest.main()
