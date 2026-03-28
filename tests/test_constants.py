from army.constants import KeywordsDict
from army.constants import Keyword, Keywords, Timing


def test_timing_json_conversion():
    t = Timing.PASSIVE
    t_json = t.to_json()
    t2 = Timing.from_json(t_json)

    assert t2.value == t.value
    assert t2.name == t.name


def test_keyword_json_conversion():
    t = Keyword.CHAMPION
    t_json = t.to_json()
    t2 = Keyword.from_json(t_json)

    assert t2.value == t.value
    assert t2.name == t.name


def test_keywords_json_conversion():
    keyword_list = [
        Keyword.CHAMPION,
        Keyword.HERO,
        Keyword.MONSTER,
        Keyword.MUSICIAN,
        Keyword.SKAVEN,
    ]
    keywords = Keywords(keyword_list)
    kw_json = keywords.to_json()
    kw2 = Keywords.from_json(kw_json)

    assert kw2.keyword_list == keywords.keyword_list


def test_keywords_json_conversion_with_empty_list():
    keyword_list: list[Keyword] = []
    keywords = Keywords(keyword_list)
    kw_json: KeywordsDict = keywords.to_json()
    kw2 = Keywords.from_json(kw_json)

    assert kw2.keyword_list == keywords.keyword_list


def test_keywords_contains():
    keyword_list = [
        Keyword.CHAMPION,
        Keyword.HERO,
        Keyword.MONSTER,
        Keyword.MUSICIAN,
        Keyword.SKAVEN,
    ]

    keywords = Keywords(keyword_list)

    assert keyword_list[0] in keywords
    assert keyword_list[1] in keywords
    assert keyword_list[2] in keywords
    assert keyword_list[3] in keywords
    assert keyword_list[4] in keywords

    assert Keyword.MASTERCLAN not in keywords
