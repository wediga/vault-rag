from vault_rag.markdown import Section, split_sections, strip_frontmatter


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


def test_text_without_heading_is_one_section() -> None:
    assert split_sections("Der vierte Planet.\n") == [Section("", "Der vierte Planet.")]


def test_heading_path_follows_levels() -> None:
    note = (
        "# Mars\nA\n## Umlaufbahn\nB\n### Bahnelemente\nC\n## Monde\nD\n# Quellen\nE\n"
    )
    assert split_sections(note) == [
        Section("Mars", "A"),
        Section("Mars > Umlaufbahn", "B"),
        Section("Mars > Umlaufbahn > Bahnelemente", "C"),
        Section("Mars > Monde", "D"),
        Section("Quellen", "E"),
    ]


def test_drops_empty_sections_but_keeps_their_heading_in_the_path() -> None:
    note = "# Mars\n\n## Umlaufbahn\nEin Umlauf dauert 687 Tage.\n## Monde\n\n"
    assert split_sections(note) == [
        Section("Mars > Umlaufbahn", "Ein Umlauf dauert 687 Tage."),
    ]


def test_hash_in_code_block_is_no_heading() -> None:
    note = "# Skript\n```bash\n# Kommentar\n```\n~~~\n# Noch einer\n~~~\n"
    assert split_sections(note) == [
        Section("Skript", "```bash\n# Kommentar\n```\n~~~\n# Noch einer\n~~~"),
    ]


def test_tag_is_no_heading() -> None:
    assert split_sections("#astronomie\nText\n") == [Section("", "#astronomie\nText")]
