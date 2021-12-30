from abc import ABC, abstractmethod
from typing import List
import pydub


class Encoder(ABC):
    NO_ENCODE = "__NO_ENCODE__"

    @abstractmethod
    def get_formats(self) -> List[str]:
        pass

    @abstractmethod
    def encode(self, data, format):
        pass


class DefaultEncoder(Encoder):
    def __init__(self):
        self.formats = ["wav", "mp3"]
        self.default_params = {
            "wav": ["-ar", "  16000"],
            "mp3": None
        }

    def get_formats(self):
        return self.formats

    def encode(self, data, format=None):
        if not format or format == self.NO_ENCODE:
            return data

        params = self.default_params[format]
        audio = pydub.AudioSegment(data)
        return audio.export(format=format, parameters=params).read()
