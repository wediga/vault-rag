import time

from vault_rag.markdown import (
    Section,
    extract_links,
    split_sections,
    strip_frontmatter,
)

# With backtracking, this many unclosed openings take seconds instead of milliseconds.
UNCLOSED_OPENINGS = 10_000
TIME_LIMIT_SECONDS = 1


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


def test_extracts_links_in_order_with_duplicates() -> None:
    text = "[[Mars]] kreist wie [[Erde]] um die Sonne, [[Mars]] weiter außen."
    assert extract_links(text) == ["Mars", "Erde", "Mars"]


def test_alias_is_dropped() -> None:
    assert extract_links("[[Mars|der rote Planet]]") == ["Mars"]


def test_section_is_dropped() -> None:
    assert extract_links("[[Mars#Umlaufbahn]]") == ["Mars"]


def test_section_and_alias_are_dropped() -> None:
    assert extract_links("[[Mars#Umlaufbahn|Marsbahn]]") == ["Mars"]


def test_embedded_note_counts_but_embedded_file_does_not() -> None:
    text = "![[Mars]]\n![[mars.png]]\n![[Bahndaten.pdf]]"
    assert extract_links(text) == ["Mars"]


def test_line_break_ends_a_link() -> None:
    assert extract_links("[[Mars\nErde]]") == []


def test_many_unclosed_links_are_fast() -> None:
    start = time.perf_counter()
    extract_links("[[" * UNCLOSED_OPENINGS)
    assert time.perf_counter() - start < TIME_LIMIT_SECONDS
