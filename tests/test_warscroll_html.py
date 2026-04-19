import re
from pathlib import Path


WARSCROLL_FILE = Path(__file__).resolve().parents[1] / "src" / "warscroll.html"
SHARED_CSS_FILE = Path(__file__).resolve().parents[1] / "src" / "styles" / "shared.css"
FORBIDDEN_PATTERNS = (
    r"<script\b",
    r"<iframe\b",
    r"googletagmanager",
    r"google-analytics",
    r"doubleclick",
    r"\bgtag\b",
    r"facebook pixel",
    r"hotjar",
    r"\bon(?:click|error|load)\s*=",
)


def test_warscroll_layout_contains_core_sections():
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


def test_warscroll_uses_shared_stylesheet():
    assert SHARED_CSS_FILE.exists()

    html = WARSCROLL_FILE.read_text(encoding="utf-8")

    assert re.search(
        r'<link[^>]*rel="stylesheet"[^>]*href="styles/shared\.css"', html, re.IGNORECASE
    )
    assert not re.search(r"<style\b", html, re.IGNORECASE)


def test_warscroll_layout_omits_scripts_iframes_and_tracking():
    html = WARSCROLL_FILE.read_text(encoding="utf-8")

    for forbidden_pattern in FORBIDDEN_PATTERNS:
        assert not re.search(forbidden_pattern, html, re.IGNORECASE)
