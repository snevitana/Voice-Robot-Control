from collections.abc import Mapping, Sequence

from voice_robot_control.commands.command import RobotCommand
from voice_robot_control.commands.normalization import normalize_text


class CommandMatcher:
    def __init__(self, commands: Mapping[RobotCommand, Sequence[str]]) -> None:
        self._phrase_to_command: dict[str, RobotCommand] = {}
        for command, phrases in commands.items():
            for phrase in phrases:
                normalized = normalize_text(phrase)
                if normalized:
                    self._phrase_to_command[normalized] = command

    def match(self, text: str) -> RobotCommand | None:
        return self._phrase_to_command.get(normalize_text(text))

    def list_phrases(self) -> dict[RobotCommand, list[str]]:
        result: dict[RobotCommand, list[str]] = {command: [] for command in RobotCommand}
        for phrase, command in self._phrase_to_command.items():
            result.setdefault(command, []).append(phrase)
        return {command: sorted(phrases) for command, phrases in result.items() if phrases}
