from typing import Protocol

from voice_robot_control.commands.command import RobotCommand


class RobotBackend(Protocol):
    def send_command(self, command: RobotCommand) -> None: ...
