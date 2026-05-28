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

from .converter.markdown_parser import parse_markdown
from .converter.docx_builder import build_docx
from .config import TemplateConfig, get_preset


def convert_markdown_to_docx(
    md_text: str,
    output_path: str,
    template: str = "课程论文",
    image_base_dir: str = "",
):
    """High-level API: Markdown text → docx file."""
    config = get_preset(template)
    blocks = parse_markdown(md_text)
    build_docx(blocks, config, output_path, image_base_dir=image_base_dir or None)
