from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
