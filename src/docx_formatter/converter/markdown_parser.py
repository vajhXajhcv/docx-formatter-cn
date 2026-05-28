"""
Lightweight Markdown parser for Chinese academic papers.

Supports:
- Headings (# ## ###)
- Paragraphs with inline formatting
- Block formulas ($$...$$) and inline formulas ($...$)
- Tables (| a | b |)
- Code blocks (```lang)
- Lists (-, 1.)
- Images ![alt](url)
- Citations [n]
- Bold **text**, italic *text*
- Page breaks (--- or <page-break>)
"""

import re
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class InlineText:
    text: str


@dataclass
class InlineBold:
    text: str


@dataclass
class InlineItalic:
    text: str


@dataclass
class InlineFormula:
    latex: str


@dataclass
class InlineCitation:
    number: str


@dataclass
class InlineImage:
    alt: str
    url: str


@dataclass
class InlineLink:
    text: str
    url: str


InlineElement = InlineText | InlineBold | InlineItalic | InlineFormula | InlineCitation | InlineImage | InlineLink


@dataclass
class BlockHeading:
    level: int
    inline: List[InlineElement]


@dataclass
class BlockParagraph:
    inline: List[InlineElement]


@dataclass
class BlockFormula:
    latex: str
    number: Optional[str] = None


@dataclass
class BlockTable:
    headers: List[str]
    rows: List[List[str]]
    alignments: List[str] = field(default_factory=list)


@dataclass
class BlockCode:
    language: Optional[str]
    lines: List[str]


@dataclass
class BlockListItem:
    level: int
    marker: str
    inline: List[InlineElement]
    ordered: bool = False


@dataclass
class BlockImage:
    alt: str
    url: str


@dataclass
class BlockBlank:
    pass


@dataclass
class BlockPageBreak:
    pass


BlockElement = (
    BlockHeading | BlockParagraph | BlockFormula | BlockTable |
    BlockCode | BlockListItem | BlockImage | BlockBlank | BlockPageBreak
)


def parse_markdown(text: str) -> List[BlockElement]:
    lines = text.splitlines()
    blocks: List[BlockElement] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Blank line
        if not stripped:
            i += 1
            continue

        # Page break
        if stripped == "---" or stripped == "***" or stripped == "<page-break>":
            blocks.append(BlockPageBreak())
            i += 1
            continue

        # Heading
        m = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if m:
            level = len(m.group(1))
            heading_text = m.group(2).strip()
            blocks.append(BlockHeading(level=level, inline=_parse_inline(heading_text)))
            i += 1
            continue

        # Block formula
        if stripped.startswith("$$"):
            if stripped.endswith("$$") and len(stripped) > 2:
                latex = stripped[2:-2].strip()
                blocks.append(_parse_block_formula(latex))
                i += 1
                continue
            else:
                latex_lines = []
                i += 1
                while i < len(lines) and not lines[i].strip().endswith("$$"):
                    latex_lines.append(lines[i])
                    i += 1
                if i < len(lines):
                    last = lines[i].strip()
                    if last.endswith("$$"):
                        latex_lines.append(last[:-2])
                    i += 1
                latex = "\n".join(latex_lines).strip()
                blocks.append(_parse_block_formula(latex))
                continue

        # Code block
        if stripped.startswith("```"):
            lang = stripped[3:].strip() or None
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            i += 1  # skip closing ```
            blocks.append(BlockCode(language=lang, lines=code_lines))
            continue

        # Table
        if "|" in stripped:
            table, new_i = _try_parse_table(lines, i)
            if table is not None:
                blocks.append(table)
                i = new_i
                continue

        # List item
        list_m = re.match(r"^(\s*)([-+*]|\d+[.、)）])\s+(.*)$", line)
        if list_m:
            indent = len(list_m.group(1))
            marker = list_m.group(2)
            item_text = list_m.group(3)
            level = indent // 2
            ordered = marker[0].isdigit()
            blocks.append(BlockListItem(
                level=level, marker=marker, inline=_parse_inline(item_text), ordered=ordered
            ))
            i += 1
            continue

        # Regular paragraph (may span multiple lines)
        para_lines = [stripped]
        i += 1
        while i < len(lines) and lines[i].strip() and not _is_block_start(lines[i]):
            para_lines.append(lines[i].strip())
            i += 1
        para_text = " ".join(para_lines)
        blocks.append(BlockParagraph(inline=_parse_inline(para_text)))

    return blocks


def _is_block_start(line: str) -> bool:
    s = line.strip()
    if not s:
        return False
    if s.startswith("#") or s.startswith("```") or s.startswith("$$") or s.startswith("|"):
        return True
    if re.match(r"^\s*([-+*]|\d+[.、)）])\s+", s):
        return True
    if s == "---" or s == "***" or s == "<page-break>":
        return True
    return False


def _parse_block_formula(latex: str) -> BlockFormula:
    """Extract optional number from end: ... \\tag{1} or ...(1)"""
    m = re.search(r"\\tag\{([^}]+)\}\s*$", latex)
    if m:
        number = m.group(1)
        latex = latex[: m.start()].strip()
        return BlockFormula(latex=latex, number=number)
    m = re.search(r"\s+\((\d+)\)\s*$", latex)
    if m:
        number = m.group(1)
        latex = latex[: m.start()].strip()
        return BlockFormula(latex=latex, number=number)
    return BlockFormula(latex=latex)


def _try_parse_table(lines: List[str], start: int) -> tuple[Optional[BlockTable], int]:
    """Try to parse a markdown table starting at lines[start]."""
    i = start
    # First row must contain |
    if "|" not in lines[i].strip():
        return None, start

    header_line = lines[i].strip()
    headers = [c.strip() for c in header_line.split("|")]
    # Remove empty first/last if line starts/ends with |
    if headers and not headers[0]:
        headers = headers[1:]
    if headers and not headers[-1]:
        headers = headers[:-1]
    if not headers:
        return None, start
    i += 1

    # Separator line (optional for our parser)
    if i < len(lines) and "|" in lines[i] and "-" in lines[i]:
        sep_line = lines[i].strip()
        align_parts = [c.strip() for c in sep_line.split("|")]
        if align_parts and not align_parts[0]:
            align_parts = align_parts[1:]
        if align_parts and not align_parts[-1]:
            align_parts = align_parts[:-1]
        alignments = []
        for p in align_parts:
            if p.startswith(":") and p.endswith(":"):
                alignments.append("center")
            elif p.endswith(":"):
                alignments.append("right")
            elif p.startswith(":"):
                alignments.append("left")
            else:
                alignments.append("left")
        i += 1
    else:
        alignments = ["left"] * len(headers)

    rows = []
    while i < len(lines) and "|" in lines[i].strip():
        row_line = lines[i].strip()
        cells = [c.strip() for c in row_line.split("|")]
        if cells and not cells[0]:
            cells = cells[1:]
        if cells and not cells[-1]:
            cells = cells[:-1]
        if len(cells) != len(headers):
            # malformed, stop
            break
        rows.append(cells)
        i += 1

    if not rows:
        return None, start

    return BlockTable(headers=headers, rows=rows, alignments=alignments), i


def _parse_inline(text: str) -> List[InlineElement]:
    """Parse inline elements: bold, italic, inline formula, citation, image, link."""
    elements: List[InlineElement] = []
    pos = 0

    # Regex for all inline patterns (ordered by priority)
    patterns = [
        (r"!\[([^\]]*)\]\(([^)]+)\)", "image"),
        (r"\[([^\]]+)\]\(([^)]+)\)", "link"),
        (r"\*\*([^\*]+?)\*\*", "bold"),
        (r"\*([^\*]+?)\*", "italic"),
        (r"\$\$([^$]+?)\$\$", "formula_display"),
        (r"\$([^$\s][^$]*?)\$", "formula"),
        (r"\[(\d+)\]", "citation"),
    ]

    while pos < len(text):
        best_match = None
        best_type = None
        best_start = len(text)

        for pat, typ in patterns:
            m = re.search(pat, text[pos:])
            if m and m.start() + pos < best_start:
                best_match = m
                best_type = typ
                best_start = m.start() + pos

        if best_match is None:
            # No more inline elements
            remaining = text[pos:]
            if remaining:
                elements.append(InlineText(remaining))
            break

        # Add text before match
        if best_start > pos:
            elements.append(InlineText(text[pos:best_start]))

        end = best_start + len(best_match.group(0))

        if best_type == "image":
            elements.append(InlineImage(alt=best_match.group(1), url=best_match.group(2)))
        elif best_type == "link":
            elements.append(InlineLink(text=best_match.group(1), url=best_match.group(2)))
        elif best_type == "bold":
            elements.append(InlineBold(best_match.group(1)))
        elif best_type == "italic":
            elements.append(InlineItalic(best_match.group(1)))
        elif best_type == "formula_display":
            elements.append(InlineFormula(best_match.group(1)))
        elif best_type == "formula":
            elements.append(InlineFormula(best_match.group(1)))
        elif best_type == "citation":
            elements.append(InlineCitation(best_match.group(1)))

        pos = end

    return elements
