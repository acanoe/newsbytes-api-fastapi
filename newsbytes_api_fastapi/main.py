from datetime import datetime

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .auth import auth_router
from .schemas import News, Story
from .sources import sources_router

# ---------------------------------- The app --------------------------------- #
app = FastAPI(
    title="Newsbytes API",
    description="FastAPI based API for newsbytes",
    version="0.0.1",
)

# ---------------------------- CORS configuration ---------------------------- #
origins = [
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ------------------------- Validation error messages ------------------------ #
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    error_messages = []
    for error in exc.errors():
        field_name = error["loc"][-1]
        error_message = error["msg"]
        error_messages.append(f"{field_name}: {error_message}")
    return JSONResponse({"error": ", ".join(error_messages)}, status_code=400)


# ---------------------------------- Routers --------------------------------- #
app.include_router(auth_router)
app.include_router(sources_router)


# ------------------------------ Main endpoints ------------------------------ #
@app.get(
    "/",
    response_model=News,
    response_model_exclude_none=True,
    response_model_exclude_unset=True,
)
def get_all_stories():
    return News(
        stories=[
            Story(
                id=1,
                date=datetime.now(),
                title="Title",
                href="https://example.com",
                hnews="http://example.com",
                tags=["tag1", "tag2"],
            ),
            Story(
                id=2,
                date=datetime.now(),
                title="Title",
                href="https://example.com",
                lobsters="http://example.com",
                tags=["tag1", "tag2"],
            ),
        ],
        tags=["tag1", "tag2"],
    )
