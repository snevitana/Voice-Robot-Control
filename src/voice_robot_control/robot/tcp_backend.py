import logging
import socket

from voice_robot_control.commands.command import RobotCommand
from voice_robot_control.config import TcpConfig

logger = logging.getLogger(__name__)


class TcpBackendError(RuntimeError):
    pass


class TcpRobotBackend:
    def __init__(self, config: TcpConfig) -> None:
        self._config = config

    def send_command(self, command: RobotCommand) -> None:
        payload = f"{command.name}\n".encode("ascii")
        try:
            with socket.create_connection(
                (self._config.host, self._config.port),
                timeout=self._config.timeout,
            ) as connection:
                connection.sendall(payload)
        except OSError as exc:
            raise TcpBackendError(
                f"TCP backend недоступен: {self._config.host}:{self._config.port}"
            ) from exc
        logger.info("Sent TCP command: %s", command.name)
