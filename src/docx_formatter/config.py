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
