from enum import StrEnum
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field, ValidationError, field_validator

from voice_robot_control.commands.command import RobotCommand


class ConfigError(RuntimeError):
    pass


class BackendName(StrEnum):
    SIMULATION = "simulation"
    SERIAL = "serial"
    TCP = "tcp"


class SerialConfig(BaseModel):
    port: str = "/dev/ttyUSB0"
    baudrate: int = 9600
    timeout: float = 1.0


class TcpConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 9000
    timeout: float = 2.0


class AppConfig(BaseModel):
    vosk_model_path: Path
    sample_rate: int = Field(default=16000, gt=0)
    audio_block_size: int = Field(default=8000, gt=0)
    backend: BackendName = BackendName.SIMULATION
    log_level: str = "INFO"
    commands: dict[RobotCommand, list[str]]
    serial: SerialConfig = Field(default_factory=SerialConfig)
    tcp: TcpConfig = Field(default_factory=TcpConfig)

    @field_validator("commands")
    @classmethod
    def validate_commands(
        cls, commands: dict[RobotCommand, list[str]]
    ) -> dict[RobotCommand, list[str]]:
        if not commands:
            raise ValueError("commands section must not be empty")
        for command, phrases in commands.items():
            if not phrases:
                raise ValueError(f"command {command.name} must contain at least one phrase")
        return commands


def load_config(path: str | Path) -> AppConfig:
    config_path = Path(path)
    if not config_path.exists():
        raise ConfigError(f"Конфиг не найден: {config_path}")

    try:
        raw_data = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ConfigError(f"Не удалось прочитать конфиг {config_path}: {exc}") from exc
    except yaml.YAMLError as exc:
        raise ConfigError(f"Некорректный YAML в конфиге {config_path}: {exc}") from exc

    if not isinstance(raw_data, dict):
        raise ConfigError(f"Конфиг {config_path} должен содержать YAML-словарь")

    try:
        data = _convert_command_keys(raw_data)
        return AppConfig.model_validate(data)
    except (ValidationError, ValueError) as exc:
        raise ConfigError(f"Некорректный конфиг {config_path}: {exc}") from exc


def _convert_command_keys(raw_data: dict[str, Any]) -> dict[str, Any]:
    data = dict(raw_data)
    raw_commands = data.get("commands")
    if not isinstance(raw_commands, dict):
        raise ValueError("commands section is required")

    commands: dict[RobotCommand, list[str]] = {}
    for key, phrases in raw_commands.items():
        try:
            command = RobotCommand[key]
        except KeyError as exc:
            available = ", ".join(command.name for command in RobotCommand)
            raise ValueError(f"unknown command {key!r}; available: {available}") from exc
        if not isinstance(phrases, list) or not all(isinstance(item, str) for item in phrases):
            raise ValueError(f"phrases for {key} must be a list of strings")
        commands[command] = phrases

    data["commands"] = commands
    return data
