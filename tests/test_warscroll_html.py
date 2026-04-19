import re
from pathlib import Path


WARSCROLL_FILE = Path(__file__).resolve().parents[1] / "src" / "warscroll.html"


def test_warscroll_layout_keeps_only_core_sections():
    html = WARSCROLL_FILE.read_text(encoding="utf-8")

    assert re.search(r'<main[^>]*class="warscroll"', html, re.IGNORECASE)
    assert re.search(
        r'<section[^>]*aria-labelledby="core-stats"', html, re.IGNORECASE
    )
    assert re.search(
        r'<section[^>]*aria-labelledby="battle-profile"', html, re.IGNORECASE
    )
    assert re.search(r'<section[^>]*aria-labelledby="weapons"', html, re.IGNORECASE)
    assert re.search(r'<section[^>]*aria-labelledby="abilities"', html, re.IGNORECASE)
    assert re.search(r'<section[^>]*aria-labelledby="keywords"', html, re.IGNORECASE)


def test_warscroll_layout_omits_embeds_and_tracking_markup():
    html = WARSCROLL_FILE.read_text(encoding="utf-8")

    for forbidden_pattern in (
        r"<script\b",
        r"<iframe\b",
        r"googletagmanager",
        r"google-analytics",
        r"doubleclick",
    ):
        assert not re.search(forbidden_pattern, html, re.IGNORECASE)
