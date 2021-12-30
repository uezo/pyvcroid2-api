from fastapi.openapi.utils import get_openapi


class OpenApiSchema:
    def __init__(self, app_routes):
        self.cache = None
        self.app_routes = app_routes

    def get_openapi(self):
        if self.cache is not None:
            return self.cache

        openapi_schema = get_openapi(
            title="pyvcroid2-api",
            version="0.1.0",
            description="A RESTful API layer to use VOICEROID2 as a service.",
            routes=self.app_routes
        )

        self.cache = openapi_schema

        return self.cache
