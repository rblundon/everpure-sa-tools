"""Tests for safemode_charts.py against the ashbpasan001 sample data."""

import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from safemode_charts import load_data, render_card, _fmt_cap, _fmt_pct

SAMPLE_XLSX = Path(__file__).parent.parent / "test.xlsx"


@pytest.fixture(scope="module")
def data():
    if not SAMPLE_XLSX.exists():
        pytest.skip("test.xlsx not present — run safemode_parser.py first")
    return load_data(SAMPLE_XLSX, only_arrays=["ashbpasan001"])


def test_load_data_array_present(data):
    assert "ashbpasan001" in data


def test_volume_counts(data):
    arr = data["ashbpasan001"]
    total = sum(arr[r]["count"] for r in arr)
    assert total == 87


def test_protected_count(data):
    assert data["ashbpasan001"]["PROTECTED"]["count"] == 0


def test_at_risk_count(data):
    assert data["ashbpasan001"]["AT RISK"]["count"] == 10


def test_critical_count(data):
    assert data["ashbpasan001"]["CRITICAL"]["count"] == 69


def test_svg_valid_xml_both(data):
    svg = render_card("ashbpasan001", data["ashbpasan001"], "both", False, "")
    ET.fromstring(svg)  # raises if invalid


def test_svg_valid_xml_count(data):
    svg = render_card("ashbpasan001", data["ashbpasan001"], "count", False, "")
    ET.fromstring(svg)


def test_svg_valid_xml_capacity(data):
    svg = render_card("ashbpasan001", data["ashbpasan001"], "capacity", False, "")
    ET.fromstring(svg)


def test_svg_contains_array_name(data):
    svg = render_card("ashbpasan001", data["ashbpasan001"], "both", False, "")
    assert "ashbpasan001" in svg


def test_svg_contains_brand_colors(data):
    svg = render_card("ashbpasan001", data["ashbpasan001"], "both", False, "")
    assert "#8FA596" in svg  # MOSS_GREEN — protected (not BP) slices
    assert "#BD673D" in svg  # CINNAMON_BROWN — at risk slices
    assert "#DEA193" in svg  # QUARTZ_PINK — critical slices
    assert "#FF7023" in svg  # PURE_ORANGE — accent bar


def test_fmt_cap():
    assert _fmt_cap(1.5) == "1.50 TB"
    assert _fmt_cap(0.5) == "512.00 GB"
    assert "MB" in _fmt_cap(0.0001)


def test_fmt_pct_small():
    assert _fmt_pct(0.5) == "&lt;1%"
    assert _fmt_pct(0) == "0%"
    assert _fmt_pct(9) == "9%"
