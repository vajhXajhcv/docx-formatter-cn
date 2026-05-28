"""
Unit tests for formula engine.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from docx_formatter.formula.mathml_to_omml import mathml_to_omml_element
from latex2mathml.converter import convert


def test_basic_formula():
    mathml = convert("x^2")
    omath = mathml_to_omml_element(mathml)
    assert omath.tag.endswith("oMath")
    # Should contain sSup
    assert any(child.tag.endswith("sSup") for child in omath)


def test_fraction():
    mathml = convert(r"\frac{a}{b}")
    omath = mathml_to_omml_element(mathml)
    assert any(child.tag.endswith("f") for child in omath)


def test_sqrt():
    mathml = convert(r"\sqrt{x}")
    omath = mathml_to_omml_element(mathml)
    assert any(child.tag.endswith("rad") for child in omath)


def test_subscript():
    mathml = convert("a_n")
    omath = mathml_to_omml_element(mathml)
    assert any(child.tag.endswith("sSub") for child in omath)


def test_accent():
    mathml = convert(r"\overline{x}")
    omath = mathml_to_omml_element(mathml)
    assert any(child.tag.endswith("acc") for child in omath)


if __name__ == "__main__":
    test_basic_formula()
    test_fraction()
    test_sqrt()
    test_subscript()
    test_accent()
    print("All formula tests passed!")
