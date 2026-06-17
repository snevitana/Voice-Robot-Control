import logging

from voice_robot_control.commands.command import RobotCommand

logger = logging.getLogger(__name__)


class SimulationRobotBackend:
    def __init__(self) -> None:
        self.history: list[RobotCommand] = []

    def send_command(self, command: RobotCommand) -> None:
        self.history.append(command)
        logger.info("Simulation backend received command: %s", command.name)
        print(command.name)
