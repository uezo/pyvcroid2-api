import threading
from pyvcroid2 import VcRoid2
from .encoder import DefaultEncoder


class FormatNotSupportedException(Exception):
    pass


class VoiceroidEngine:
    __instance = None
    __lock = threading.Lock()

    @classmethod
    def setup(cls, speaker_name=None, *, encoder=None, volume=1.0,
              speed=1.0, pitch=1.0, emphasis=1.0, pause_middle=150,
              pause_long=370, pause_sentence=800, master_volume=1.0):

        cls.__instance = cls(
            speaker_name, encoder=encoder, volume=volume, speed=speed,
            pitch=pitch, emphasis=emphasis, pause_middle=pause_middle,
            pause_long=pause_long, pause_sentence=pause_sentence,
            master_volume=master_volume
        )

    @classmethod
    def get_instance(cls):
        with cls.__lock:
            if cls.__instance is None:
                cls.setup()
        return cls.__instance

    def __init__(self, speaker_name=None, *, encoder=None, volume=1.0,
                 speed=1.0, pitch=1.0, emphasis=1.0, pause_middle=150,
                 pause_long=370, pause_sentence=800, master_volume=1.0):

        self.vcroid = VcRoid2()

        # Load language
        languages = self.vcroid.listLanguages()
        if "standard" in languages:
            self.vcroid.loadLanguage("standard")
        elif 0 < len(languages):
            self.vcroid.loadLanguage(languages[0])
        else:
            raise Exception("Language not found")

        # Load voice library
        voices = self.vcroid.listVoices()
        if not voices:
            raise Exception("Voice library not found")
        elif speaker_name:
            if speaker_name in voices:
                self.vcroid.loadVoice(speaker_name)
            else:
                raise Exception(f"Voice library for {speaker_name} not found")
        else:
            self.vcroid.loadVoice(voices[0])

        # Update settings
        self.update_settings(volume, speed, pitch, emphasis, pause_middle,
                             pause_long, pause_sentence, master_volume)

        self.encoder = encoder or DefaultEncoder()
        self.cache = {self.encoder.NO_ENCODE: {}}
        for k in self.encoder.get_formats():
            self.cache[k] = {}

    def update_settings(self, volume=None, speed=None, pitch=None,
                        emphasis=None, pause_middle=None, pause_long=None,
                        pause_sentence=None, master_volume=None):
        if volume is not None:
            self.vcroid.param.volume = volume
        if speed is not None:
            self.vcroid.param.speed = speed
        if pitch is not None:
            self.vcroid.param.pitch = pitch
        if emphasis is not None:
            self.vcroid.param.emphasis = emphasis
        if pause_middle is not None:
            self.vcroid.param.pauseMiddle = pause_middle
        if pause_long is not None:
            self.vcroid.param.pauseLong = pause_long
        if pause_sentence is not None:
            self.vcroid.param.pauseSentence = pause_sentence
        if master_volume is not None:
            self.vcroid.param.masterVolume = master_volume

    def get_voice(self, text, format=None, **params):
        format = format or self.encoder.NO_ENCODE

        if format not in self.cache.keys():
            raise FormatNotSupportedException(f"Encoding '{format}' is not supported")

        if text in self.cache[format] and not params:
            return self.cache[format][text]

        if params:
            self.update_settings(**params)

        voice, _ = self.vcroid.textToSpeech(text)

        encoded_voice = self.encoder.encode(voice, format)
        self.cache[format][text] = encoded_voice
        return encoded_voice

    def clear_cache(self):
        self.cache.clear()
