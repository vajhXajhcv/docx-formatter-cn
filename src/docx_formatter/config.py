"""
Template / configuration system for docx-formatter-cn.

Supports presets: 毕业论文, 课程论文, 数学建模, 公文
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, List


@dataclass
class FontConfig:
    chinese: str = "SimSun"
    english: str = "Cambria Math"
    heading_chinese: str = "SimHei"
    heading_english: str = "Cambria Math"
    code: str = "Consolas"


@dataclass
class PageConfig:
    width_mm: float = 210.0  # A4
    height_mm: float = 297.0
    margin_top_mm: float = 25.0
    margin_bottom_mm: float = 25.0
    margin_left_mm: float = 25.0
    margin_right_mm: float = 25.0
    header_distance_mm: float = 15.0
    footer_distance_mm: float = 15.0


@dataclass
class HeadingConfig:
    h1_size_pt: int = 16  #三号
    h2_size_pt: int = 14  #四号
    h3_size_pt: int = 12  #小四
    h4_size_pt: int = 12
    bold: bool = True
    alignment: str = "left"  # center for h1 in some templates


@dataclass
class BodyConfig:
    size_pt: int = 12  #小四
    line_spacing: float = 1.5
    first_line_indent_chars: float = 2.0
    alignment: str = "justify"


@dataclass
class TableConfig:
    three_line: bool = True
    header_border_width_pt: float = 1.5
    bottom_border_width_pt: float = 1.5
    inner_border_width_pt: float = 0.0
    font_size_pt: int = 10  #五号
    repeat_header: bool = True


@dataclass
class FormulaConfig:
    font: str = "Cambria Math"
    number_in_paren: bool = True


@dataclass
class CaptionConfig:
    figure_prefix: str = "图"
    table_prefix: str = "表"
    font_size_pt: int = 10
    bold: bool = True
    alignment: str = "center"


@dataclass
class ReferenceConfig:
    numbering_style: str = "decimal_bracket"  # [1], [2]
    font_size_pt: int = 10
    hanging_indent_mm: float = 10.0


@dataclass
class TemplateConfig:
    name: str = "default"
    description: str = ""
    page: PageConfig = field(default_factory=PageConfig)
    font: FontConfig = field(default_factory=FontConfig)
    heading: HeadingConfig = field(default_factory=HeadingConfig)
    body: BodyConfig = field(default_factory=BodyConfig)
    table: TableConfig = field(default_factory=TableConfig)
    formula: FormulaConfig = field(default_factory=FormulaConfig)
    caption: CaptionConfig = field(default_factory=CaptionConfig)
    reference: ReferenceConfig = field(default_factory=ReferenceConfig)
    header_text: Optional[str] = None
    footer_page_number: bool = True
    toc_enabled: bool = True


def get_preset(name: str) -> TemplateConfig:
    presets = {
        "default": TemplateConfig(name="default", description="默认模板"),
        "课程论文": _course_paper(),
        "毕业论文": _thesis(),
        "数学建模": _mcm(),
        "公文": _official(),
    }
    return presets.get(name, presets["default"])


def load_template_from_json(path: str) -> TemplateConfig:
    """Load a TemplateConfig from a JSON file."""
    import json
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return _dict_to_config(data)


def load_template_from_yaml(path: str) -> TemplateConfig:
    """Load a TemplateConfig from a YAML file."""
    import yaml
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return _dict_to_config(data)


def _dict_to_config(data: dict) -> TemplateConfig:
    """Build TemplateConfig from a flat dict with dot-notation keys."""
    cfg = TemplateConfig(
        name=data.get("name", "custom"),
        description=data.get("description", ""),
    )

    def _set(obj, key, value):
        parts = key.split(".")
        for part in parts[:-1]:
            obj = getattr(obj, part)
        setattr(obj, parts[-1], value)

    # Page
    for k in ["width_mm", "height_mm", "margin_top_mm", "margin_bottom_mm",
              "margin_left_mm", "margin_right_mm", "header_distance_mm", "footer_distance_mm"]:
        if k in data:
            _set(cfg, f"page.{k}", data[k])

    # Font
    for k in ["chinese", "english", "heading_chinese", "heading_english", "code"]:
        if k in data:
            _set(cfg, f"font.{k}", data[k])

    # Heading
    for k in ["h1_size_pt", "h2_size_pt", "h3_size_pt", "h4_size_pt", "bold", "alignment"]:
        if k in data:
            _set(cfg, f"heading.{k}", data[k])

    # Body
    for k in ["size_pt", "line_spacing", "first_line_indent_chars", "alignment"]:
        if k in data:
            _set(cfg, f"body.{k}", data[k])

    # Table
    for k in ["three_line", "header_border_width_pt", "bottom_border_width_pt",
              "inner_border_width_pt", "font_size_pt", "repeat_header"]:
        if k in data:
            _set(cfg, f"table.{k}", data[k])

    # Formula
    for k in ["font", "number_in_paren"]:
        if k in data:
            _set(cfg, f"formula.{k}", data[k])

    # Caption
    for k in ["figure_prefix", "table_prefix", "font_size_pt", "bold", "alignment"]:
        if k in data:
            _set(cfg, f"caption.{k}", data[k])

    # Other top-level
    for k in ["header_text", "footer_page_number", "toc_enabled"]:
        if k in data:
            setattr(cfg, k, data[k])

    return cfg


def _course_paper() -> TemplateConfig:
    cfg = TemplateConfig(
        name="课程论文",
        description="中国大陆高校课程论文/毕业设计模板",
        page=PageConfig(
            margin_top_mm=25.0,
            margin_bottom_mm=25.0,
            margin_left_mm=25.0,
            margin_right_mm=25.0,
        ),
        font=FontConfig(
            chinese="SimSun",
            english="Cambria Math",
            heading_chinese="SimHei",
            heading_english="Cambria Math",
        ),
        heading=HeadingConfig(
            h1_size_pt=16,
            h2_size_pt=14,
            h3_size_pt=12,
            bold=True,
            alignment="left",
        ),
        body=BodyConfig(
            size_pt=12,
            line_spacing=1.5,
            first_line_indent_chars=2.0,
            alignment="justify",
        ),
        table=TableConfig(
            three_line=True,
            header_border_width_pt=1.5,
            bottom_border_width_pt=1.5,
            inner_border_width_pt=0.0,
            font_size_pt=10,
        ),
        caption=CaptionConfig(
            figure_prefix="图",
            table_prefix="表",
            font_size_pt=10,
            bold=True,
            alignment="center",
        ),
        footer_page_number=True,
        toc_enabled=True,
    )
    return cfg


def _thesis() -> TemplateConfig:
    cfg = _course_paper()
    cfg.name = "毕业论文"
    cfg.description = "学位论文/毕业论文排版模板"
    cfg.heading.h1_size_pt = 22  # 二号
    cfg.heading.h2_size_pt = 16  # 三号
    cfg.heading.h3_size_pt = 14  # 四号
    cfg.body.line_spacing = 1.5
    cfg.page.margin_top_mm = 25.0
    cfg.page.margin_bottom_mm = 25.0
    cfg.page.margin_left_mm = 30.0
    cfg.page.margin_right_mm = 25.0
    return cfg


def _mcm() -> TemplateConfig:
    cfg = _course_paper()
    cfg.name = "数学建模"
    cfg.description = "数学建模竞赛论文模板"
    cfg.body.line_spacing = 1.0
    cfg.page.margin_left_mm = 20.0
    cfg.page.margin_right_mm = 20.0
    return cfg


def _official() -> TemplateConfig:
    cfg = _course_paper()
    cfg.name = "公文"
    cfg.description = "GB/T 公文格式模板"
    cfg.font.chinese = "仿宋"
    cfg.font.heading_chinese = "方正小标宋简体"
    cfg.heading.h1_size_pt = 22
    cfg.heading.h2_size_pt = 16
    cfg.body.size_pt = 16
    cfg.body.line_spacing = 1.5
    cfg.body.first_line_indent_chars = 2.0
    return cfg
