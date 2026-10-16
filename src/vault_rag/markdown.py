import re

# Only a block at the very start counts, so a horizontal rule (---) in the text stays.
# \r? because notes saved on Windows end their lines with \r\n.
FRONTMATTER = re.compile(r"\A---\r?\n.*?^---\r?$\n?", re.MULTILINE | re.DOTALL)


def strip_frontmatter(text: str) -> str:
    return FRONTMATTER.sub("", text, count=1)
