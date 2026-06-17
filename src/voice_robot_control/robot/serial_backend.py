import logging

from voice_robot_control.commands.command import RobotCommand
from voice_robot_control.config import SerialConfig

logger = logging.getLogger(__name__)


class SerialBackendError(RuntimeError):
    pass


class SerialRobotBackend:
    def __init__(self, config: SerialConfig) -> None:
        try:
            import serial
            from serial import SerialException
        except ImportError as exc:
            raise SerialBackendError(
                "Не установлен pyserial. Выполните: pip install pyserial"
            ) from exc

        self._serial_exception_type = SerialException
        try:
            self._connection = serial.Serial(
                port=config.port,
                baudrate=config.baudrate,
                timeout=config.timeout,
            )
        except SerialException as exc:
            raise SerialBackendError(
                f"Serial-порт недоступен: {config.port}. Проверьте порт и права доступа."
            ) from exc

    def send_command(self, command: RobotCommand) -> None:
        payload = f"{command.name}\n".encode("ascii")
        try:
            self._connection.write(payload)
            self._connection.flush()
        except self._serial_exception_type as exc:
            raise SerialBackendError(
                f"Не удалось отправить команду в serial backend: {exc}"
            ) from exc
        logger.info("Sent serial command: %s", command.name)

    def close(self) -> None:
        self._connection.close()
