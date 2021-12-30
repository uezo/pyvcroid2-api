from pydantic import BaseModel, Field


class VoiceParams(BaseModel):
    volume: float = Field(None, description="Volume", example=1.23)
    speed: float = Field(None, description="Speed", example=0.987)
    pitch: float = Field(None, description="Pitch", example=1.111)
    emphasis: float = Field(None, description="Emphasis", example=0.893)
    pause_middle: float = Field(None, description="PauseMiddle. Applied after \"、\" etc.", example=80)
    pause_long: float = Field(None, description="PauseLong. Applied after \"。\" etc.", example=100)
    pause_sentence: float = Field(None, description="PauseSentence. Silent margin after speech.", example=200)
    master_volume: float = Field(None, description="Master volume", example=1.123)


class VoiceRequest(BaseModel):
    text: str = Field(..., description="Text to speech", example="こんにちは。")
    format: str = Field(None, description="Format of audio encoding", example="mp3")
    params: VoiceParams = Field(None, description="VOICEROID parameters", example={"volume": 1.5, "speed": 0.95, "pitch": 1.05})


class ApiError(BaseModel):
    message: str = Field(..., description="Error message", example="Text is missing for speech-to-text")
    detail: dict = Field(None, description="Detail information for debugging")
