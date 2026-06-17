from collections.abc import Iterator
from typing import Protocol


class AudioSource(Protocol):
    def chunks(self) -> Iterator[bytes]: ...
