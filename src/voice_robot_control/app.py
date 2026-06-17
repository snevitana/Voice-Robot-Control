import logging

from voice_robot_control.audio.microphone import MicrophoneAudioSource
from voice_robot_control.commands.matcher import CommandMatcher
from voice_robot_control.config import AppConfig, BackendName
from voice_robot_control.robot.backend import RobotBackend
from voice_robot_control.robot.serial_backend import SerialRobotBackend
from voice_robot_control.robot.simulation_backend import SimulationRobotBackend
from voice_robot_control.robot.tcp_backend import TcpRobotBackend
from voice_robot_control.speech.vosk_recognizer import VoskSpeechRecognizer

logger = logging.getLogger(__name__)


def build_matcher(config: AppConfig) -> CommandMatcher:
    return CommandMatcher(config.commands)


def build_backend(config: AppConfig) -> RobotBackend:
    if config.backend is BackendName.SIMULATION:
        return SimulationRobotBackend()
    if config.backend is BackendName.SERIAL:
        return SerialRobotBackend(config.serial)
    if config.backend is BackendName.TCP:
        return TcpRobotBackend(config.tcp)
    raise ValueError(f"Unsupported backend: {config.backend}")


def process_text(text: str, matcher: CommandMatcher, backend: RobotBackend) -> bool:
    command = matcher.match(text)
    if command is None:
        logger.warning("Команда не распознана: %s", text)
        return False
    backend.send_command(command)
    return True


def run_microphone_loop(config: AppConfig) -> None:
    audio_source = MicrophoneAudioSource(
        sample_rate=config.sample_rate,
        block_size=config.audio_block_size,
    )
    recognizer = VoskSpeechRecognizer(config.vosk_model_path, config.sample_rate)
    matcher = build_matcher(config)
    backend = build_backend(config)

    logger.info("Listening for voice commands")
    for text in recognizer.recognize_stream(audio_source.chunks()):
        logger.info("Recognized text: %s", text)
        process_text(text, matcher, backend)
