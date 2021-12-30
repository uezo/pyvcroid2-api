import pytest
import os
from uuid import uuid4
import pydub
from pyvcroid2api.encoder import DefaultEncoder


class TestEncoder:
    def test_get_formats(self):
        encoder = DefaultEncoder()
        assert len(encoder.formats) == 2

    def test_encode(self):
        with open("testvoice.wav", "rb") as f:
            data = f.read()

        encoder = DefaultEncoder()

        # No encode
        voice = encoder.encode(data)
        audio = pydub.AudioSegment(data=voice)

        assert len(voice) > 90000
        assert audio.channels == 1
        assert audio.frame_rate == 44100

        # Wave 22050Hz
        voice = encoder.encode(data, format="wav")
        audio = pydub.AudioSegment(data=voice)

        assert len(voice) < 90000
        assert len(voice) > 30000
        assert audio.channels == 1
        assert audio.frame_rate == 16000

        # MP3
        voice = encoder.encode(data, format="mp3")
        filename = f"{str(uuid4())}.mp3"
        with open(filename, "wb") as f:
            f.write(voice)
        audio = pydub.AudioSegment.from_mp3(filename)

        assert len(voice) < 30000
        assert len(voice) > 9000
        assert audio.channels == 1
        assert audio.frame_rate == 44100

        os.remove(filename)

        # Unknown
        with pytest.raises(Exception):
            encoder.encode("string data that cannot be converted to mp3", format="mp3")
