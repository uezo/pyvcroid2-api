import traceback
from logging import getLogger
from fastapi import APIRouter, Depends
from fastapi.exceptions import RequestValidationError
from pydantic.main import BaseModel
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from .schemas import VoiceParams, VoiceRequest, ApiError
from .engine import VoiceroidEngine, FormatNotSupportedException


router = APIRouter()


@router.post("/api/speech",
             description="Get the speech-to-text voice by VOICEROID2",
             responses={
                200: {
                    "content": {"audio/wav": {}, "audio/mpeg": {}},
                    "description": "Return the audio data of text-to-speech."
                },
                400: {
                    "content": {"application/json": {
                        "example": {
                            "message": "Validation error",
                            "detail": {"errors": [{"loc": ["body", "text"], "msg": "none is not an allowed value", "type": "type_error.none.not_allowed"}]}
                        }
                    }},
                    "description": "Required field is missing or the type is invalid"
                },
                422: {
                    "content": {"application/json": {
                        "example": {
                            "message": "Encoding 'ogg' is not supported",
                            "detail": None
                        }
                    }},
                    "description": "Unsupported Encoding"
                },
                500: {
                    "content": {"application/json": {
                        "example": {
                            "message": "Error occurs in doing something: XXX is missing",
                            "detail": None
                        }
                    }},
                    "description": "Server Error"
                },
             })
async def get_voice(
        request: VoiceRequest,
        vcengine: VoiceroidEngine = Depends(VoiceroidEngine.get_instance)):

    if request.params:
        voice = vcengine.get_voice(
            text=request.text, format=request.format,
            **request.params.dict()
        )
    else:
        voice = vcengine.get_voice(
            text=request.text, format=request.format
        )

    return Response(content=voice)


@router.patch("/api/settings",
              description="Update settings",
              response_model=BaseModel, responses={422: {}})
async def update_settings(
        request: VoiceParams,
        vcengine: VoiceroidEngine = Depends(VoiceroidEngine.get_instance)):

    vcengine.update_settings(**request.params)
    return JSONResponse({})


@router.get("/api/settings",
            description="Get current settings",
            response_model=VoiceParams)
async def get_settings(
        vcengine: VoiceroidEngine = Depends(VoiceroidEngine.get_instance)):

    params = VoiceParams(
        volume=vcengine.vcroid.param.volume,
        speed=vcengine.vcroid.param.speed,
        pitch=vcengine.vcroid.param.pitch,
        emphasis=vcengine.vcroid.param.emphasis,
        pause_middle=vcengine.vcroid.param.pauseMiddle,
        pause_long=vcengine.vcroid.param.pauseLong,
        pause_sentence=vcengine.vcroid.param.pauseSentence,
        master_volume=vcengine.vcroid.param.masterVolume,
    )

    return JSONResponse(params.json())


@router.delete("/api/cache",
               description="Delete all cached voices",
               response_model=BaseModel)
async def delete_cache(
        vcengine: VoiceroidEngine = Depends(VoiceroidEngine.get_instance)):

    vcengine.clear_cache()
    return JSONResponse({})


async def validation_error_handler(request: Request, ex: RequestValidationError):
    err = ApiError(message="Validation error", detail={"errors": ex.errors()})
    return JSONResponse(content=err.json(), status_code=400)


async def default_exception_handler(request: Request, ex: Exception):
    err = ApiError(message=str(ex))
    getLogger(__name__).error(f"{str(ex)}: {traceback.format_exc()}")
    return JSONResponse(
        content=err.json(),
        status_code=422 if isinstance(ex, FormatNotSupportedException) else 500)
