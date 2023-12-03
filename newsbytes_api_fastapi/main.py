from typing import Optional

from celery import Celery
from fastapi import Depends, FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from .auth import auth_router
from .config import settings
from .database import Base, engine
from .dependencies import get_db
from .models import stories
from .schemas import News
from .sources import sources_router

# ---------------------------- Database migration ---------------------------- #
Base.metadata.create_all(bind=engine)

# -------------------------------- Celery app -------------------------------- #
celery_app = Celery("worker", broker="amqp://rabbitmq:rabbitmq@localhost:5672")

# -------------------------------- FastAPI app ------------------------------- #
app = FastAPI(
    title="Newsbytes API",
    description="FastAPI based API for newsbytes",
    version="0.0.1",
)

# ---------------------------- CORS configuration ---------------------------- #
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
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
def get_all_stories(tags: Optional[list[str]] = None, db: Session = Depends(get_db)):
    news_stories = stories.get_by_tag(db, tags=tags) if tags else stories.get_multi(db)
    tags = set([story.tags for story in news_stories])

    return News(
        stories=news_stories,
        tags=list(tags),
    )
