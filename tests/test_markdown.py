"""
Unit tests for Markdown parser.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from docx_formatter.converter.markdown_parser import (
    parse_markdown, BlockHeading, BlockParagraph, BlockFormula,
    BlockTable, BlockListItem, InlineFormula, InlineCitation, InlineBold,
    InlineCode, InlineLink,
)


def test_heading():
    blocks = parse_markdown("# Title\n## Section")
    assert len(blocks) == 2
    assert isinstance(blocks[0], BlockHeading)
    assert blocks[0].level == 1
    assert isinstance(blocks[1], BlockHeading)
    assert blocks[1].level == 2


def test_paragraph_with_inline():
    blocks = parse_markdown("This is **bold** and $x^2$ and [1]")
    assert len(blocks) == 1
    para = blocks[0]
    assert isinstance(para, BlockParagraph)
    # Check inline elements
    types = [type(e).__name__ for e in para.inline]
    assert "InlineBold" in types
    assert "InlineFormula" in types
    assert "InlineCitation" in types


def test_formula_block():
    blocks = parse_markdown("$$E = mc^2$$")
    assert len(blocks) == 1
    assert isinstance(blocks[0], BlockFormula)
    assert blocks[0].latex == "E = mc^2"


def test_table():
    text = "| A | B |\n|---|---|\n| 1 | 2 |"
    blocks = parse_markdown(text)
    assert len(blocks) == 1
    assert isinstance(blocks[0], BlockTable)
    assert blocks[0].headers == ["A", "B"]
    assert blocks[0].rows == [["1", "2"]]


def test_list():
    blocks = parse_markdown("- item 1\n- item 2")
    assert len(blocks) == 2
    assert isinstance(blocks[0], BlockListItem)
    assert isinstance(blocks[1], BlockListItem)


def test_inline_code():
    blocks = parse_markdown("Use `print()` to output.")
    assert len(blocks) == 1
    para = blocks[0]
    assert isinstance(para, BlockParagraph)
    types = [type(e).__name__ for e in para.inline]
    assert "InlineCode" in types
    code_elem = [e for e in para.inline if isinstance(e, InlineCode)][0]
    assert code_elem.text == "print()"


def test_inline_link():
    blocks = parse_markdown("See [docs](https://example.com).")
    assert len(blocks) == 1
    para = blocks[0]
    assert isinstance(para, BlockParagraph)
    types = [type(e).__name__ for e in para.inline]
    assert "InlineLink" in types
    link_elem = [e for e in para.inline if isinstance(e, InlineLink)][0]
    assert link_elem.text == "docs"
    assert link_elem.url == "https://example.com"


if __name__ == "__main__":
    test_heading()
    test_paragraph_with_inline()
    test_formula_block()
    test_table()
    test_list()
    test_inline_code()
    test_inline_link()
    print("All markdown tests passed!")
