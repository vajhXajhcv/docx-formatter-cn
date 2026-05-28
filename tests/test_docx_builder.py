"""
Unit tests for docx_builder.
"""

import sys
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from docx_formatter.converter.markdown_parser import parse_markdown
from docx_formatter.converter.docx_builder import build_docx
from docx_formatter.config import get_preset


def test_build_docx_basic():
    md = "# Title\n\nHello world.\n\n| A | B |\n|---|---|\n| 1 | 2 |"
    blocks = parse_markdown(md)
    config = get_preset("课程论文")
    with tempfile.TemporaryDirectory() as tmpdir:
        out = Path(tmpdir) / "test.docx"
        build_docx(blocks, config, str(out))
        assert out.exists()
        assert out.stat().st_size > 0


def test_build_docx_with_formula():
    md = "$$E = mc^2$$\n\n$x^2$"
    blocks = parse_markdown(md)
    config = get_preset("课程论文")
    with tempfile.TemporaryDirectory() as tmpdir:
        out = Path(tmpdir) / "test.docx"
        build_docx(blocks, config, str(out))
        assert out.exists()


if __name__ == "__main__":
    test_build_docx_basic()
    test_build_docx_with_formula()
    print("All docx_builder tests passed!")
