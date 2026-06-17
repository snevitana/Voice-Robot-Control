from voice_robot_control.commands.normalization import normalize_text


def test_normalize_text_lowercase_punctuation_and_spaces() -> None:
    assert normalize_text("  Поверни, НАЛЕВО!  ") == "поверни налево"


def test_normalize_text_replaces_yo() -> None:
    assert normalize_text("Едь ещё вперёд") == "едь еще вперед"


def test_normalize_text_keeps_cyrillic() -> None:
    assert normalize_text("двигайся назад") == "двигайся назад"
