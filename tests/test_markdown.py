from vault_rag.markdown import strip_frontmatter


def test_removes_frontmatter() -> None:
    note = "---\ntags: [astronomie]\n---\n# Mars\nDer vierte Planet.\n"
    assert strip_frontmatter(note) == "# Mars\nDer vierte Planet.\n"


def test_keeps_note_without_frontmatter() -> None:
    note = "# Mars\nDer vierte Planet.\n"
    assert strip_frontmatter(note) == note


def test_keeps_rule_in_the_middle_of_the_text() -> None:
    note = "# Mars\nOben\n---\nUnten\n---\n"
    assert strip_frontmatter(note) == note


def test_keeps_unclosed_frontmatter() -> None:
    note = "---\ntags: [astronomie]\n# Mars\n"
    assert strip_frontmatter(note) == note


def test_removes_frontmatter_with_windows_line_endings() -> None:
    note = "---\r\ntags: [astronomie]\r\n---\r\n# Mars\r\n"
    assert strip_frontmatter(note) == "# Mars\r\n"
