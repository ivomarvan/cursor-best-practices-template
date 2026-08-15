"""Parser and emitter for the constrained YAML subset used by intent nodes.

The intent tree deliberately restricts its front matter so that it can be parsed
without third-party dependencies: mappings, sequences of scalars, sequences of
mappings, quoted or bare scalars, integers, booleans and null. Anchors, tags,
multi-line block scalars and nested flow collections are rejected with an error
rather than silently ignored.
"""

from __future__ import annotations


class YamlError(Exception):
    """Raised when the input leaves the supported YAML subset."""

    def __init__(self, line: int, message: str) -> None:
        super().__init__(f"line {line}: {message}")
        self.line = line
        self.message = message


def strip_comment(text: str) -> str:
    """Remove a trailing ``#`` comment while respecting quoted strings."""
    quote: str | None = None
    for index, char in enumerate(text):
        if quote:
            if char == quote:
                quote = None
        elif char in ('"', "'"):
            quote = char
        elif char == "#" and (index == 0 or text[index - 1] in " \t"):
            return text[:index]
    return text


def _split_flow(body: str, line: int) -> list[str]:
    """Split a flow collection body on commas outside quotes."""
    parts: list[str] = []
    current: list[str] = []
    quote: str | None = None
    for char in body:
        if quote:
            current.append(char)
            if char == quote:
                quote = None
            continue
        if char in ('"', "'"):
            quote = char
            current.append(char)
        elif char in "[]{}":
            raise YamlError(line, "nested flow collections are not supported")
        elif char == ",":
            parts.append("".join(current))
            current = []
        else:
            current.append(char)
    if quote:
        raise YamlError(line, "unterminated quoted string")
    tail = "".join(current)
    if tail.strip() or parts:
        parts.append(tail)
    return parts


def parse_scalar(text: str, line: int) -> object:
    """Parse a single scalar, a flow sequence or a flow mapping."""
    value = text.strip()
    if value == "":
        return None
    if value.startswith("["):
        if not value.endswith("]"):
            raise YamlError(line, "unterminated flow sequence")
        return [parse_scalar(item, line) for item in _split_flow(value[1:-1], line)]
    if value.startswith("{"):
        if not value.endswith("}"):
            raise YamlError(line, "unterminated flow mapping")
        mapping: dict[str, object] = {}
        for item in _split_flow(value[1:-1], line):
            if ":" not in item:
                raise YamlError(line, f"flow mapping entry without ':': {item!r}")
            key, _, raw = item.partition(":")
            mapping[key.strip()] = parse_scalar(raw, line)
        return mapping
    if value[0] in ('"', "'"):
        if len(value) < 2 or value[-1] != value[0]:
            raise YamlError(line, "unterminated quoted string")
        return value[1:-1]
    if value in ("null", "~"):
        return None
    if value == "true":
        return True
    if value == "false":
        return False
    if value.startswith("&") or value.startswith("*") or value.startswith("!"):
        raise YamlError(line, "anchors, aliases and tags are not supported")
    if value in ("|", ">"):
        raise YamlError(line, "block scalars are not supported")
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        pass
    return value


class _Line:
    __slots__ = ("indent", "number", "text")

    def __init__(self, indent: int, text: str, number: int) -> None:
        self.indent = indent
        self.text = text
        self.number = number


def _scan(text: str) -> list[_Line]:
    lines: list[_Line] = []
    for number, raw in enumerate(text.splitlines(), start=1):
        if "\t" in raw[: len(raw) - len(raw.lstrip())]:
            raise YamlError(number, "tabs are not allowed for indentation")
        stripped = strip_comment(raw).rstrip()
        if not stripped.strip():
            continue
        if stripped.strip() == "---":
            continue
        indent = len(stripped) - len(stripped.lstrip())
        lines.append(_Line(indent, stripped.strip(), number))
    return lines


class _Parser:
    def __init__(self, lines: list[_Line]) -> None:
        self.lines = lines
        self.pos = 0

    def at_end(self) -> bool:
        return self.pos >= len(self.lines)

    def peek(self) -> _Line:
        return self.lines[self.pos]

    def parse_block(self, indent: int) -> object:
        if self.at_end():
            return None
        if self.peek().text.startswith("- "):
            return self.parse_sequence(indent)
        return self.parse_mapping(indent)

    def parse_mapping(self, indent: int) -> dict[str, object]:
        result: dict[str, object] = {}
        while not self.at_end():
            line = self.peek()
            if line.indent < indent:
                break
            if line.indent > indent:
                raise YamlError(line.number, "unexpected indentation")
            if line.text.startswith("- "):
                break
            if ":" not in line.text:
                raise YamlError(line.number, f"expected 'key: value', got {line.text!r}")
            key, _, raw = line.text.partition(":")
            key = key.strip()
            if not key:
                raise YamlError(line.number, "empty key")
            self.pos += 1
            if raw.strip() == "":
                if not self.at_end() and self.peek().indent > indent:
                    result[key] = self.parse_block(self.peek().indent)
                else:
                    result[key] = None
            else:
                result[key] = parse_scalar(raw, line.number)
        return result

    def parse_sequence(self, indent: int) -> list[object]:
        items: list[object] = []
        while not self.at_end():
            line = self.peek()
            if line.indent < indent or not line.text.startswith("- "):
                break
            if line.indent > indent:
                raise YamlError(line.number, "unexpected indentation in sequence")
            inline = line.text[2:].strip()
            self.pos += 1
            if ":" in inline and not inline.startswith(("'", '"', "[", "{")):
                items.append(self._sequence_mapping(inline, line, indent))
            else:
                items.append(parse_scalar(inline, line.number))
        return items

    def _sequence_mapping(self, inline: str, line: _Line, indent: int) -> dict[str, object]:
        key, _, raw = inline.partition(":")
        mapping: dict[str, object] = {}
        child_indent = indent + 2
        if not self.at_end() and self.lines[self.pos].indent > indent:
            child_indent = self.lines[self.pos].indent
        if raw.strip() == "" and not self.at_end() and self.peek().indent > indent:
            mapping[key.strip()] = self.parse_block(self.peek().indent)
        else:
            mapping[key.strip()] = parse_scalar(raw, line.number)
        while not self.at_end():
            following = self.peek()
            if following.indent != child_indent or following.text.startswith("- "):
                break
            if ":" not in following.text:
                raise YamlError(following.number, "expected 'key: value' inside sequence item")
            sub_key, _, sub_raw = following.text.partition(":")
            self.pos += 1
            if sub_raw.strip() == "" and not self.at_end() and self.peek().indent > child_indent:
                mapping[sub_key.strip()] = self.parse_block(self.peek().indent)
            else:
                mapping[sub_key.strip()] = parse_scalar(sub_raw, following.number)
        return mapping


def parse(text: str) -> dict[str, object]:
    """Parse a YAML document from the supported subset into a dictionary."""
    lines = _scan(text)
    if not lines:
        return {}
    parser = _Parser(lines)
    value = parser.parse_block(lines[0].indent)
    if not parser.at_end():
        raise YamlError(parser.peek().number, "trailing content after document")
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise YamlError(lines[0].number, "document root must be a mapping")
    return value


def split_front_matter(text: str) -> tuple[str, str]:
    """Split a Markdown file into its front matter block and its body."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise YamlError(1, "file does not start with '---' front matter")
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return "\n".join(lines[1:index]), "\n".join(lines[index + 1 :])
    raise YamlError(1, "front matter is not terminated by '---'")


def _emit_scalar(value: object) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value)
    needs_quotes = (
        text == ""
        or text[0] in "[]{}#&*!|>'\"%@`-?:,"
        or ": " in text
        or text.strip() != text
        or text in ("true", "false", "null", "~")
    )
    if needs_quotes:
        escaped = text.replace('"', '\\"')
        return f'"{escaped}"'
    return text


def dump(data: dict[str, object]) -> str:
    """Emit a mapping using the same restricted subset the parser accepts."""
    out: list[str] = []

    def emit_mapping(mapping: dict[str, object], indent: int) -> None:
        pad = " " * indent
        for key, value in mapping.items():
            if isinstance(value, dict):
                if not value:
                    out.append(f"{pad}{key}: {{}}")
                    continue
                out.append(f"{pad}{key}:")
                emit_mapping(value, indent + 2)
            elif isinstance(value, list):
                if not value:
                    out.append(f"{pad}{key}: []")
                    continue
                if all(isinstance(item, dict) for item in value):
                    out.append(f"{pad}{key}:")
                    for item in value:
                        emit_sequence_mapping(item, indent + 2)
                else:
                    inline = ", ".join(_emit_scalar(item) for item in value)
                    out.append(f"{pad}{key}: [{inline}]")
            else:
                out.append(f"{pad}{key}: {_emit_scalar(value)}")

    def emit_sequence_mapping(item: dict[str, object], indent: int) -> None:
        pad = " " * indent
        first = True
        for key, value in item.items():
            prefix = f"{pad}- " if first else f"{pad}  "
            first = False
            if isinstance(value, (dict, list)):
                raise YamlError(0, "nested collections inside sequence items are not supported")
            out.append(f"{prefix}{key}: {_emit_scalar(value)}")

    emit_mapping(data, 0)
    return "\n".join(out) + "\n"
