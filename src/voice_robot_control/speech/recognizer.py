from collections.abc import Iterable, Iterator
from typing import Protocol


class SpeechRecognizer(Protocol):
    def recognize_stream(self, audio_chunks: Iterable[bytes]) -> Iterator[str]: ...
