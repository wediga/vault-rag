import re
from typing import NamedTuple

# Only a block at the very start counts, so a horizontal rule (---) in the text stays.
# \r? because notes saved on Windows end their lines with \r\n.
FRONTMATTER = re.compile(r"\A---\r?\n.*?^---\r?$\n?", re.MULTILINE | re.DOTALL)
# The space after the hashes separates a heading from an Obsidian tag like #astronomie.
HEADING = re.compile(r"^(#{1,6}) +(.+?)\s*$")
CODE_FENCE = re.compile(r"^(```|~~~)")
HEADING_SEPARATOR = " > "


class Section(NamedTuple):
    heading: str
    text: str


def strip_frontmatter(text: str) -> str:
    return FRONTMATTER.sub("", text, count=1)


def split_sections(text: str) -> list[Section]:
    """Split at headings; each section carries the path of headings above it."""
    sections = []
    path: list[tuple[int, str]] = []
    lines: list[str] = []
    open_fence = None

    for line in text.splitlines():
        if open_fence:
            if line.startswith(open_fence):
                open_fence = None
        elif fence := CODE_FENCE.match(line):
            open_fence = fence.group(1)
        elif heading := HEADING.match(line):
            sections.append(_section(path, lines))
            level = len(heading.group(1))
            path = [(lvl, title) for lvl, title in path if lvl < level]
            path.append((level, heading.group(2)))
            lines = []

            continue
        lines.append(line)
    sections.append(_section(path, lines))

    return [section for section in sections if section.text]


def _section(path: list[tuple[int, str]], lines: list[str]) -> Section:
    heading = HEADING_SEPARATOR.join(title for _, title in path)

    return Section(heading, "\n".join(lines).strip())
