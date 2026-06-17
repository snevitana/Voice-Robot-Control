from pathlib import Path

import pytest

from voice_robot_control.commands.command import RobotCommand
from voice_robot_control.config import BackendName, ConfigError, load_config


def test_load_pc_config() -> None:
    config = load_config(Path("configs/pc_simulation.yaml"))

    assert config.backend is BackendName.SIMULATION
    assert config.sample_rate == 16000
    assert RobotCommand.MOVE_FORWARD in config.commands


def test_missing_config_raises_clear_error(tmp_path: Path) -> None:
    with pytest.raises(ConfigError, match="Конфиг не найден"):
        load_config(tmp_path / "missing.yaml")


def test_unknown_command_key_raises_config_error(tmp_path: Path) -> None:
    config_path = tmp_path / "bad.yaml"
    config_path.write_text(
        """
vosk_model_path: models/vosk-model-small-ru-0.22
commands:
  FLY:
    - лети
""",
        encoding="utf-8",
    )

    with pytest.raises(ConfigError, match="unknown command"):
        load_config(config_path)
