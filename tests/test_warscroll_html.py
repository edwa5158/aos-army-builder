from pathlib import Path


WARSCR0LL_FILE = Path(__file__).resolve().parents[1] / "src" / "warscroll.html"


def test_warscroll_layout_keeps_only_core_sections():
    html = WARSCR0LL_FILE.read_text(encoding="utf-8").lower()

    assert '<main class="warscroll">' in html
    assert ">core stats<" in html
    assert ">battle profile<" in html
    assert ">weapons<" in html
    assert ">abilities<" in html
    assert ">keywords<" in html


def test_warscroll_layout_omits_embeds_and_tracking_markup():
    html = WARSCR0LL_FILE.read_text(encoding="utf-8").lower()

    for forbidden_fragment in ("<script", "<iframe", "analytics", "googletagmanager", "ads"):
        assert forbidden_fragment not in html
