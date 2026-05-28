"""
MathML → OMML (Office Math Markup Language) converter.

Ported from docx-skill-4-cn-paper's mathml-to-docx.js logic.
Generates native Word formula XML that can be inserted via python-docx's lxml.
"""

from lxml import etree

MATH_NS = "http://schemas.openxmlformats.org/officeDocument/2006/math"
MATHML_NS = "http://www.w3.org/1998/Math/MathML"


def mathml_to_omml_element(mathml_str: str) -> etree.Element:
    """Parse a MathML string and return an <m:oMath> lxml Element."""
    # Remove XML declaration if present
    s = mathml_str.strip()
    if s.startswith("<?xml"):
        s = s[s.find(">") + 1 :].strip()
    root = etree.fromstring(s.encode("utf-8"))
    omath = etree.Element("{%s}oMath" % MATH_NS)
    _walk(root, omath)
    return omath


def _local_name(elem: etree.Element) -> str:
    return etree.QName(elem).localname


def _text_content(elem: etree.Element) -> str:
    """Get direct text content of an element (concatenating text nodes)."""
    parts = []
    if elem.text:
        parts.append(elem.text)
    for child in elem:
        if child.tail:
            parts.append(child.tail)
    return "".join(parts)


def _children(elem: etree.Element) -> list:
    """Return child elements (skip text nodes at this level)."""
    return list(elem)


def _walk(node: etree.Element, parent: etree.Element):
    """Recursively convert MathML node to OMML, appending to parent."""
    tag = _local_name(node)

    if tag == "math":
        for child in _children(node):
            _walk(child, parent)
        return

    if tag == "mrow":
        for child in _children(node):
            _walk(child, parent)
        return

    if tag in ("mi", "mn", "mo", "mtext"):
        _make_run(parent, _text_content(node) or (node.text or ""))
        return

    if tag == "msup":
        kids = _children(node)
        if len(kids) >= 2:
            ssup = etree.SubElement(parent, "{%s}sSup" % MATH_NS)
            e = etree.SubElement(ssup, "{%s}e" % MATH_NS)
            _walk(kids[0], e)
            sup = etree.SubElement(ssup, "{%s}sup" % MATH_NS)
            _walk(kids[1], sup)
        return

    if tag == "msub":
        kids = _children(node)
        if len(kids) >= 2:
            ssub = etree.SubElement(parent, "{%s}sSub" % MATH_NS)
            e = etree.SubElement(ssub, "{%s}e" % MATH_NS)
            _walk(kids[0], e)
            sub = etree.SubElement(ssub, "{%s}sub" % MATH_NS)
            _walk(kids[1], sub)
        return

    if tag == "msubsup":
        kids = _children(node)
        if len(kids) >= 3:
            ssubsup = etree.SubElement(parent, "{%s}sSubSup" % MATH_NS)
            e = etree.SubElement(ssubsup, "{%s}e" % MATH_NS)
            _walk(kids[0], e)
            sub = etree.SubElement(ssubsup, "{%s}sub" % MATH_NS)
            _walk(kids[1], sub)
            sup = etree.SubElement(ssubsup, "{%s}sup" % MATH_NS)
            _walk(kids[2], sup)
        return

    if tag == "mfrac":
        kids = _children(node)
        if len(kids) >= 2:
            frac = etree.SubElement(parent, "{%s}f" % MATH_NS)
            num = etree.SubElement(frac, "{%s}num" % MATH_NS)
            _walk(kids[0], num)
            den = etree.SubElement(frac, "{%s}den" % MATH_NS)
            _walk(kids[1], den)
        return

    if tag == "msqrt":
        kids = _children(node)
        rad = etree.SubElement(parent, "{%s}rad" % MATH_NS)
        # square root has no degree
        if kids:
            e = etree.SubElement(rad, "{%s}e" % MATH_NS)
            _walk(kids[0], e)
        return

    if tag == "mroot":
        kids = _children(node)
        if len(kids) >= 2:
            rad = etree.SubElement(parent, "{%s}rad" % MATH_NS)
            deg = etree.SubElement(rad, "{%s}deg" % MATH_NS)
            _walk(kids[1], deg)
            e = etree.SubElement(rad, "{%s}e" % MATH_NS)
            _walk(kids[0], e)
        return

    if tag == "munder":
        kids = _children(node)
        if len(kids) >= 2:
            op_text = _extract_text(kids[0])
            if "∑" in op_text or "∏" in op_text or "∫" in op_text:
                nary = etree.SubElement(parent, "{%s}nary" % MATH_NS)
                # base operator as run inside e? Actually nary needs sub/sup and e
                # For munder: sub only
                sub = etree.SubElement(nary, "{%s}sub" % MATH_NS)
                _walk(kids[1], sub)
                sup = etree.SubElement(nary, "{%s}sup" % MATH_NS)
                # empty sup
                _make_run(sup, "")
                e = etree.SubElement(nary, "{%s}e" % MATH_NS)
                _walk(kids[0], e)
            else:
                # fallback: limLow
                limlow = etree.SubElement(parent, "{%s}limLow" % MATH_NS)
                e = etree.SubElement(limlow, "{%s}e" % MATH_NS)
                _walk(kids[0], e)
                lim = etree.SubElement(limlow, "{%s}lim" % MATH_NS)
                _walk(kids[1], lim)
        return

    if tag == "mover":
        kids = _children(node)
        if len(kids) >= 2:
            op_text = _extract_text(kids[0])
            if "∑" in op_text or "∏" in op_text or "∫" in op_text:
                nary = etree.SubElement(parent, "{%s}nary" % MATH_NS)
                sub = etree.SubElement(nary, "{%s}sub" % MATH_NS)
                _make_run(sub, "")
                sup = etree.SubElement(nary, "{%s}sup" % MATH_NS)
                _walk(kids[1], sup)
                e = etree.SubElement(nary, "{%s}e" % MATH_NS)
                _walk(kids[0], e)
            else:
                # fallback: limUpp
                limupp = etree.SubElement(parent, "{%s}limUpp" % MATH_NS)
                e = etree.SubElement(limupp, "{%s}e" % MATH_NS)
                _walk(kids[0], e)
                lim = etree.SubElement(limupp, "{%s}lim" % MATH_NS)
                _walk(kids[1], lim)
        return

    if tag == "munderover":
        kids = _children(node)
        if len(kids) >= 3:
            op_text = _extract_text(kids[0])
            if "∑" in op_text or "∏" in op_text or "∫" in op_text:
                nary = etree.SubElement(parent, "{%s}nary" % MATH_NS)
                sub = etree.SubElement(nary, "{%s}sub" % MATH_NS)
                _walk(kids[1], sub)
                sup = etree.SubElement(nary, "{%s}sup" % MATH_NS)
                _walk(kids[2], sup)
                e = etree.SubElement(nary, "{%s}e" % MATH_NS)
                _walk(kids[0], e)
            else:
                # fallback: render sequentially
                _walk(kids[0], parent)
                _walk(kids[1], parent)
                _walk(kids[2], parent)
        return

    if tag == "mtable":
        rows = [c for c in _children(node) if _local_name(c) == "mtr"]
        if rows:
            matrix = etree.SubElement(parent, "{%s}m" % MATH_NS)
            for row in rows:
                mr = etree.SubElement(matrix, "{%s}mr" % MATH_NS)
                cells = [c for c in _children(row) if _local_name(c) == "mtd"]
                for cell in cells:
                    me = etree.SubElement(mr, "{%s}e" % MATH_NS)
                    for child in _children(cell):
                        _walk(child, me)
        return

    if tag == "mfenced":
        # fallback: just render children sequentially
        for child in _children(node):
            _walk(child, parent)
        return

    if tag == "mspace":
        _make_run(parent, " ")
        return

    if tag == "mstyle":
        for child in _children(node):
            _walk(child, parent)
        return

    if tag == "mpadded":
        for child in _children(node):
            _walk(child, parent)
        return

    if tag == "menclose":
        for child in _children(node):
            _walk(child, parent)
        return

    if tag == "maction":
        # Use first child
        kids = _children(node)
        if kids:
            _walk(kids[0], parent)
        return

    if tag == "none":
        return

    # Unknown tag: try to walk children
    for child in _children(node):
        _walk(child, parent)


def _make_run(parent: etree.Element, text: str):
    if not text:
        return
    r = etree.SubElement(parent, "{%s}r" % MATH_NS)
    t = etree.SubElement(r, "{%s}t" % MATH_NS)
    # Preserve spaces
    if text.startswith(" ") or text.endswith(" "):
        t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    t.text = text


def _extract_text(node: etree.Element) -> str:
    """Extract all text from a MathML node recursively."""
    parts = []
    if node.text:
        parts.append(node.text)
    for child in node:
        parts.append(_extract_text(child))
        if child.tail:
            parts.append(child.tail)
    return "".join(parts)
