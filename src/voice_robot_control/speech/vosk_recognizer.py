import json
from collections.abc import Iterable, Iterator
from pathlib import Path
from typing import Any, cast


class VoskRecognizerError(RuntimeError):
    pass


class VoskSpeechRecognizer:
    def __init__(self, model_path: str | Path, sample_rate: int) -> None:
        self._model_path = Path(model_path)
        if not self._model_path.exists():
            raise VoskRecognizerError(
                f"Не найдена модель Vosk: {self._model_path}\n"
                "Скачайте модель командой: ./scripts/download_vosk_model.sh"
            )

        try:
            from vosk import KaldiRecognizer, Model, SetLogLevel
        except ImportError as exc:
            raise VoskRecognizerError("Не установлен vosk. Выполните: pip install vosk") from exc

        SetLogLevel(-1)
        self._recognizer = KaldiRecognizer(Model(str(self._model_path)), sample_rate)

    def recognize_stream(self, audio_chunks: Iterable[bytes]) -> Iterator[str]:
        for chunk in audio_chunks:
            if self._recognizer.AcceptWaveform(chunk):
                result = self._decode_result(self._recognizer.Result())
                if result:
                    yield result

    @staticmethod
    def _decode_result(raw_json: str) -> str:
        try:
            data = cast(dict[str, Any], json.loads(raw_json))
        except json.JSONDecodeError:
            return ""
        text = data.get("text")
        return text if isinstance(text, str) else ""
