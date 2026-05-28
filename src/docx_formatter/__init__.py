"""
docx-formatter-cn: Chinese academic document formatter.

Convert Markdown to beautifully formatted Word documents with:
- Native Word formulas (OMML) from LaTeX
- Three-line tables
- Chinese academic typography (SimSun/SimHei + Cambria Math)
- Auto-numbering headings, figures, tables, equations
- Template system for thesis, course paper, modeling competition, official docs
"""

__version__ = "0.1.0"

from .converter.markdown_parser import parse_markdown, parse_markdown_with_meta
from .converter.docx_builder import build_docx
from .formatter import format_existing_docx
from .config import TemplateConfig, get_preset


def convert_markdown_to_docx(
    md_text: str,
    output_path: str,
    template: str = "课程论文",
    image_base_dir: str = "",
):
    """High-level API: Markdown text → docx file."""
    config = get_preset(template)
    meta, blocks = parse_markdown_with_meta(md_text)
    build_docx(blocks, config, output_path, image_base_dir=image_base_dir or None, meta=meta)


def format_docx(
    input_path: str,
    output_path: str,
    template: str = "课程论文",
    add_toc: bool = False,
):
    """High-level API: Format existing docx with template."""
    config = get_preset(template)
    format_existing_docx(input_path, output_path, config, add_toc=add_toc)
