from army.constants import Keywords, Timing


def test_timing_json_conversion():
    t = Timing.PASSIVE
    t_json = t.to_json()
    t2 = Timing.from_json(t_json)

    assert t2.value == t.value
    assert t2.name == t.name


def test_Keywords_json_conversion():
    t = Keywords.CHAMPION
    t_json = t.to_json()
    t2 = Keywords.from_json(t_json)

    assert t2.value == t.value
    assert t2.name == t.name
