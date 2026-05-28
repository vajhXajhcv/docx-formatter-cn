"""
Command-line interface for docx-formatter-cn.
"""

import argparse
import sys
from pathlib import Path

from .converter.markdown_parser import parse_markdown, parse_markdown_with_meta
from .converter.docx_builder import build_docx
from .config import get_preset, load_template_from_json, load_template_from_yaml


def main():
    from . import __version__
    parser = argparse.ArgumentParser(
        description="docx-formatter-cn: Chinese academic document formatter",
        prog="docx-formatter",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # convert command
    convert_parser = subparsers.add_parser("convert", help="Convert Markdown to docx")
    convert_parser.add_argument("input", help="Input Markdown file path")
    convert_parser.add_argument("-o", "--output", required=True, help="Output docx file path")
    convert_parser.add_argument(
        "-t", "--template", default="课程论文",
        choices=["课程论文", "毕业论文", "数学建模", "公文", "default"],
        help="Template preset to use",
    )
    convert_parser.add_argument(
        "--template-file", default="",
        help="Custom template JSON/YAML file path (overrides --template)"
    )
    convert_parser.add_argument(
        "--image-dir", default="", help="Base directory for resolving relative image paths"
    )

    # format command
    format_parser = subparsers.add_parser("format", help="Format existing docx with template")
    format_parser.add_argument("input", help="Input docx file path")
    format_parser.add_argument("-o", "--output", required=True, help="Output docx file path")
    format_parser.add_argument(
        "-t", "--template", default="课程论文",
        choices=["课程论文", "毕业论文", "数学建模", "公文", "default"],
        help="Template preset to apply",
    )
    format_parser.add_argument(
        "--template-file", default="",
        help="Custom template JSON/YAML file path (overrides --template)"
    )
    format_parser.add_argument("--add-toc", action="store_true", help="Insert table of contents")

    # batch command
    batch_parser = subparsers.add_parser("batch", help="Batch convert all Markdown files in a directory")
    batch_parser.add_argument("input_dir", help="Input directory containing .md files")
    batch_parser.add_argument("-o", "--output-dir", required=True, help="Output directory for .docx files")
    batch_parser.add_argument(
        "-t", "--template", default="课程论文",
        choices=["课程论文", "毕业论文", "数学建模", "公文", "default"],
        help="Template preset to use",
    )
    batch_parser.add_argument(
        "--template-file", default="",
        help="Custom template JSON/YAML file path (overrides --template)"
    )
    batch_parser.add_argument(
        "--image-dir", default="", help="Base directory for resolving relative image paths"
    )

    # info command
    info_parser = subparsers.add_parser("info", help="Show template info")
    info_parser.add_argument(
        "-t", "--template", default="课程论文",
        choices=["课程论文", "毕业论文", "数学建模", "公文", "default"],
        help="Template preset to inspect",
    )

    # export-template command
    export_parser = subparsers.add_parser("export-template", help="Export a preset template to JSON")
    export_parser.add_argument(
        "-t", "--template", default="课程论文",
        choices=["课程论文", "毕业论文", "数学建模", "公文", "default"],
        help="Template preset to export",
    )
    export_parser.add_argument("-o", "--output", required=True, help="Output JSON file path")

    args = parser.parse_args()

    if args.command == "info":
        cfg = get_preset(args.template)
        print(f"Template: {cfg.name}")
        print(f"Description: {cfg.description}")
        print(f"Page: {cfg.page.width_mm}x{cfg.page.height_mm} mm")
        print(f"Margins: T{cfg.page.margin_top_mm} B{cfg.page.margin_bottom_mm} L{cfg.page.margin_left_mm} R{cfg.page.margin_right_mm} mm")
        print(f"Body font: {cfg.body.size_pt}pt, line spacing {cfg.body.line_spacing}")
        print(f"Heading sizes: H1={cfg.heading.h1_size_pt}pt H2={cfg.heading.h2_size_pt}pt H3={cfg.heading.h3_size_pt}pt")
        return

    if args.command == "export-template":
        import json
        cfg = get_preset(args.template)
        data = {
            "name": cfg.name,
            "description": cfg.description,
            "width_mm": cfg.page.width_mm,
            "height_mm": cfg.page.height_mm,
            "margin_top_mm": cfg.page.margin_top_mm,
            "margin_bottom_mm": cfg.page.margin_bottom_mm,
            "margin_left_mm": cfg.page.margin_left_mm,
            "margin_right_mm": cfg.page.margin_right_mm,
            "header_distance_mm": cfg.page.header_distance_mm,
            "footer_distance_mm": cfg.page.footer_distance_mm,
            "chinese": cfg.font.chinese,
            "english": cfg.font.english,
            "heading_chinese": cfg.font.heading_chinese,
            "heading_english": cfg.font.heading_english,
            "code": cfg.font.code,
            "h1_size_pt": cfg.heading.h1_size_pt,
            "h2_size_pt": cfg.heading.h2_size_pt,
            "h3_size_pt": cfg.heading.h3_size_pt,
            "h4_size_pt": cfg.heading.h4_size_pt,
            "bold": cfg.heading.bold,
            "size_pt": cfg.body.size_pt,
            "line_spacing": cfg.body.line_spacing,
            "first_line_indent_chars": cfg.body.first_line_indent_chars,
            "three_line": cfg.table.three_line,
            "header_border_width_pt": cfg.table.header_border_width_pt,
            "bottom_border_width_pt": cfg.table.bottom_border_width_pt,
            "inner_border_width_pt": cfg.table.inner_border_width_pt,
            "font_size_pt": cfg.table.font_size_pt,
            "repeat_header": cfg.table.repeat_header,
            "figure_prefix": cfg.caption.figure_prefix,
            "table_prefix": cfg.caption.table_prefix,
            "footer_page_number": cfg.footer_page_number,
            "toc_enabled": cfg.toc_enabled,
        }
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Template exported to: {args.output}")
        return

    def _resolve_config(args):
        if getattr(args, "template_file", ""):
            tf = Path(args.template_file)
            if not tf.exists():
                print(f"Error: template file not found: {args.template_file}", file=sys.stderr)
                sys.exit(1)
            suffix = tf.suffix.lower()
            if suffix == ".json":
                return load_template_from_json(str(tf))
            elif suffix in (".yaml", ".yml"):
                return load_template_from_yaml(str(tf))
            else:
                print("Error: template file must be .json or .yaml", file=sys.stderr)
                sys.exit(1)
        return get_preset(args.template)

    if args.command == "convert":
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"Error: input file not found: {args.input}", file=sys.stderr)
            sys.exit(1)

        md_text = input_path.read_text(encoding="utf-8")
        config = _resolve_config(args)
        meta, blocks = parse_markdown_with_meta(md_text)

        image_dir = args.image_dir or str(input_path.parent)
        build_docx(blocks, config, args.output, image_base_dir=image_dir, meta=meta)
        print(f"Saved: {args.output}")
        return

    if args.command == "format":
        from .formatter import format_existing_docx
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"Error: input file not found: {args.input}", file=sys.stderr)
            sys.exit(1)
        config = _resolve_config(args)
        format_existing_docx(str(input_path), args.output, config, add_toc=args.add_toc)
        print(f"Formatted and saved: {args.output}")
        return

    if args.command == "batch":
        input_dir = Path(args.input_dir)
        output_dir = Path(args.output_dir)
        if not input_dir.exists() or not input_dir.is_dir():
            print(f"Error: input directory not found: {args.input_dir}", file=sys.stderr)
            sys.exit(1)
        output_dir.mkdir(parents=True, exist_ok=True)
        config = _resolve_config(args)
        md_files = sorted(input_dir.glob("*.md"))
        if not md_files:
            print("No .md files found in input directory.")
            return
        success = 0
        failed = 0
        for md_file in md_files:
            out_file = output_dir / f"{md_file.stem}.docx"
            try:
                md_text = md_file.read_text(encoding="utf-8")
                meta, blocks = parse_markdown_with_meta(md_text)
                image_dir = args.image_dir or str(md_file.parent)
                build_docx(blocks, config, str(out_file), image_base_dir=image_dir, meta=meta)
                print(f"  [OK] {md_file.name} -> {out_file.name}")
                success += 1
            except Exception as e:
                print(f"  [FAIL] {md_file.name}: {e}")
                failed += 1
        print(f"\nBatch complete: {success} succeeded, {failed} failed.")
        return


if __name__ == "__main__":
    main()
