import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from src.config.settings import Settings
from src.config.db import init_db
from src.routes import add_routers


def create_app(_config: Settings):
    _app = FastAPI()

    origins = ["*"]

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @_app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
        )

    @_app.get("/")
    def index():
        return {"message": "FastAPI starter template, Use freely"}

    add_routers(app=_app, config=_config)
    return _app


# Load configuration
config = Settings.load_config()

# Create app
app = create_app(config)

app.mount('/invoices', StaticFiles(directory="invoices"), name="static")

# Initialize database
init_db(app)

if __name__ == '__main__':
    uvicorn.run("main:app", port=config.PORT, reload=True)
