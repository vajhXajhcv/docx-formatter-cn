"""
Command-line interface for docx-formatter-cn.
"""

import argparse
import sys
from pathlib import Path

from .converter.markdown_parser import parse_markdown
from .converter.docx_builder import build_docx
from .config import get_preset, load_template_from_json, load_template_from_yaml


def main():
    parser = argparse.ArgumentParser(
        description="docx-formatter-cn: Chinese academic document formatter"
    )
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

    # info command
    info_parser = subparsers.add_parser("info", help="Show template info")
    info_parser.add_argument(
        "-t", "--template", default="课程论文",
        choices=["课程论文", "毕业论文", "数学建模", "公文", "default"],
        help="Template preset to inspect",
    )

    args = parser.parse_args()

    if args.command == "info":
        cfg = get_preset(args.template)
        print(f"Template: {cfg.name}")
        print(f"Description: {cfg.description}")
        print(f"Page: {cfg.page.width_mm}×{cfg.page.height_mm} mm")
        print(f"Margins: T{cfg.page.margin_top_mm} B{cfg.page.margin_bottom_mm} L{cfg.page.margin_left_mm} R{cfg.page.margin_right_mm} mm")
        print(f"Body font: {cfg.body.size_pt}pt, line spacing {cfg.body.line_spacing}")
        print(f"Heading sizes: H1={cfg.heading.h1_size_pt}pt H2={cfg.heading.h2_size_pt}pt H3={cfg.heading.h3_size_pt}pt")
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
        blocks = parse_markdown(md_text)

        image_dir = args.image_dir or str(input_path.parent)
        build_docx(blocks, config, args.output, image_base_dir=image_dir)
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


if __name__ == "__main__":
    main()
