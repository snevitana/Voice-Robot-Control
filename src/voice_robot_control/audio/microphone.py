from collections.abc import Iterator
from queue import Queue
from typing import Any


class MicrophoneError(RuntimeError):
    pass


class MicrophoneAudioSource:
    def __init__(self, sample_rate: int, block_size: int) -> None:
        self._sample_rate = sample_rate
        self._block_size = block_size

    def chunks(self) -> Iterator[bytes]:
        try:
            import sounddevice as sd
        except ImportError as exc:
            raise MicrophoneError(
                "Не установлен sounddevice. Установите portaudio и выполните: "
                "pip install sounddevice"
            ) from exc

        audio_queue: Queue[bytes] = Queue()

        def callback(indata: Any, _frames: int, _time: Any, status: Any) -> None:
            if status:
                raise MicrophoneError(f"Ошибка микрофона: {status}")
            audio_queue.put(bytes(indata))

        try:
            with sd.RawInputStream(
                samplerate=self._sample_rate,
                blocksize=self._block_size,
                dtype="int16",
                channels=1,
                callback=callback,
            ):
                while True:
                    yield audio_queue.get()
        except Exception as exc:
            if isinstance(exc, MicrophoneError):
                raise
            raise MicrophoneError(
                "Микрофон недоступен. Проверьте устройство ввода и системные зависимости."
            ) from exc
