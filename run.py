import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from pyvcroid2api.controllers import (
    router,
    validation_error_handler,
    default_exception_handler
)
from pyvcroid2api.engine import VoiceroidEngine
from pyvcroid2api.openapi import OpenApiSchema

# # You can set the parameters here if you want
# VoiceroidEngine.setup(volume=2.0, speed=0.95, pitch=0.985, emphasis=0.97)

# Create app
app = FastAPI()

# Set controllers and exception handlers
app.include_router(router)
app.add_exception_handler(RequestValidationError, validation_error_handler)
app.add_exception_handler(Exception, default_exception_handler)

# Set OpenAPI document definitions
app.openapi = OpenApiSchema(app.routes).get_openapi


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
