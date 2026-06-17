from voice_robot_control.commands.command import RobotCommand
from voice_robot_control.commands.matcher import CommandMatcher


def test_match_exact_normalized_phrase() -> None:
    matcher = CommandMatcher({RobotCommand.TURN_LEFT: ["поверни налево"]})

    assert matcher.match("  Поверни, НАЛЕВО!  ") is RobotCommand.TURN_LEFT


def test_match_unknown_returns_none() -> None:
    matcher = CommandMatcher({RobotCommand.STOP: ["стоп"]})

    assert matcher.match("включи свет") is None


def test_list_phrases_returns_normalized_phrases() -> None:
    matcher = CommandMatcher({RobotCommand.STOP: ["Стой!", "остановись"]})

    assert matcher.list_phrases()[RobotCommand.STOP] == ["остановись", "стой"]
