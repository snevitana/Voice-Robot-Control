from voice_robot_control.commands.command import RobotCommand
from voice_robot_control.robot.simulation_backend import SimulationRobotBackend


def test_simulation_backend_saves_history(capsys) -> None:  # type: ignore[no-untyped-def]
    backend = SimulationRobotBackend()

    backend.send_command(RobotCommand.STOP)

    assert backend.history == [RobotCommand.STOP]
    assert "STOP" in capsys.readouterr().out
