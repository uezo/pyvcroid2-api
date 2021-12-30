import pytest
import os
from uuid import uuid4
import pydub
from pyvcroid2api.encoder import DefaultEncoder
from pyvcroid2api.engine import VoiceroidEngine


class CustomEncoder(DefaultEncoder):
    pass


@pytest.fixture
def engine():
    return VoiceroidEngine.get_instance()


"""
NOTE: Each test case depends on the case executed before because VoiceroidEngine is Singleton.
"""


class TestEngine:
    def test_0_singleton(self):
        # Get instance without setup (internally setup without args)
        engine_without_setup = VoiceroidEngine.get_instance()
        assert engine_without_setup.vcroid.param.pauseMiddle == 150

        # Close vcroid for following tests
        engine_without_setup.vcroid.__del__()   # close() is not exposed

        # Setup with args
        VoiceroidEngine.setup(
            speaker_name=None, encoder=CustomEncoder(),
            volume=1.1, speed=1.2, pitch=1.3, emphasis=1.4, pause_middle=100,
            pause_long=200, pause_sentence=300, master_volume=2
        )

        # Get instance after setup
        engine = VoiceroidEngine.get_instance()
        assert isinstance(engine.encoder, CustomEncoder)
        params = engine.vcroid.param
        assert round(params.volume, 1) == 1.1
        assert round(params.speed, 1) == 1.2
        assert round(params.pitch, 1) == 1.3
        assert round(params.emphasis, 1) == 1.4
        assert params.pauseMiddle == 100
        assert params.pauseLong == 200
        assert params.pauseSentence == 300
        assert params.masterVolume == 2

    def test_1_update_settings(self, engine: VoiceroidEngine):
        engine.update_settings(
            volume=1.9, speed=3.9, pitch=1.9, emphasis=1.9, pause_middle=200,
            pause_long=400, pause_sentence=600, master_volume=3
        )

        # Normal
        params = engine.vcroid.param
        assert round(params.volume, 1) == 1.9
        assert round(params.speed, 1) == 3.9
        assert round(params.pitch, 1) == 1.9
        assert round(params.emphasis, 1) == 1.9
        assert params.pauseMiddle == 200
        assert params.pauseLong == 400
        assert params.pauseSentence == 600
        assert params.masterVolume == 3

        # Over the max
        engine.update_settings(
            volume=10.0, speed=10.0, pitch=10.0, emphasis=10.0,
            pause_middle=1000000, pause_long=1000000,
            pause_sentence=1000000, master_volume=10.0
        )

        params = engine.vcroid.param
        assert round(params.volume, 1) == 2.0
        assert round(params.speed, 1) == 4.0
        assert round(params.pitch, 1) == 2.0
        assert round(params.emphasis, 1) == 2.0
        assert params.pauseMiddle == 500
        assert params.pauseLong == 2000
        assert params.pauseSentence == 10000
        assert params.masterVolume == 5.0

        # Zero
        engine.update_settings(
            volume=0, speed=0, pitch=0, emphasis=0,
            pause_middle=0, pause_long=0,
            pause_sentence=0, master_volume=0
        )

        params = engine.vcroid.param
        assert round(params.volume, 1) == 0
        assert round(params.speed, 1) == 0.5
        assert round(params.pitch, 1) == 0.5
        assert round(params.emphasis, 1) == 0
        assert params.pauseMiddle == 80
        assert params.pauseLong == 100
        assert params.pauseSentence == 200
        assert params.masterVolume == 0

        # Negative
        engine.update_settings(
            volume=-1.1, speed=-1.2, pitch=-1.3, emphasis=-1.4,
            pause_middle=-100, pause_long=-200,
            pause_sentence=-300, master_volume=-2.0
        )

        params = engine.vcroid.param
        assert round(params.volume, 1) == 0
        assert round(params.speed, 1) == 0.5
        assert round(params.pitch, 1) == 0.5
        assert round(params.emphasis, 1) == 0
        assert params.pauseMiddle == 80
        assert params.pauseLong == 100
        assert params.pauseSentence == 200
        assert params.masterVolume == 0

        # Partly update
        engine.update_settings(
            volume=1.1, speed=0.95, pitch=0.97, emphasis=1.0, master_volume=2.0
        )

        params = engine.vcroid.param
        assert round(params.volume, 1) == 1.1
        assert round(params.speed, 2) == 0.95
        assert round(params.pitch, 2) == 0.97
        assert round(params.emphasis, 1) == 1.0
        assert params.pauseMiddle == 80
        assert params.pauseLong == 100
        assert params.pauseSentence == 200
        assert params.masterVolume == 2.0

    def test_2_get_voice(self, engine: VoiceroidEngine):
        # No encode
        voice = engine.get_voice("これはテストです")
        audio = pydub.AudioSegment(data=voice)

        assert len(voice) > 90000
        assert audio.channels == 1
        assert audio.frame_rate == 44100

        # Wave 16000Hz
        voice = engine.get_voice("これはテストです", format="wav")
        audio = pydub.AudioSegment(data=voice)

        assert len(voice) < 90000
        assert len(voice) > 30000
        assert audio.channels == 1
        assert audio.frame_rate == 16000

        # MP3
        voice = engine.get_voice("これはテストです", format="mp3")
        filename = f"{str(uuid4())}.mp3"
        with open(filename, "wb") as f:
            f.write(voice)
        audio = pydub.AudioSegment.from_mp3(filename)

        assert len(voice) < 30000
        assert len(voice) > 9000
        assert audio.channels == 1
        assert audio.frame_rate == 44100

        os.remove(filename)

        # Use cache
        engine.vcroid.__del__()
        voice = engine.get_voice("これはテストです", format="wav")
        audio = pydub.AudioSegment(data=voice)

        assert len(voice) < 90000
        assert len(voice) > 30000
        assert audio.channels == 1
        assert audio.frame_rate == 16000

        with pytest.raises(Exception):
            engine.get_voice("テストです", format="wav")

    def test_3_clear_cache(self, engine: VoiceroidEngine):
        # Use cache
        engine.vcroid.__del__()
        voice = engine.get_voice("これはテストです", format="wav")
        audio = pydub.AudioSegment(data=voice)

        assert len(voice) < 90000
        assert len(voice) > 30000
        assert audio.channels == 1
        assert audio.frame_rate == 16000

        engine.clear_cache()

        with pytest.raises(Exception):
            engine.get_voice("これはテストです", format="wav")
