from datetime import datetime
from typing import Dict
from uuid import UUID
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, conint

from .models import StatsEntry

from .orm import init

app = FastAPI(title="Mangadex Stats", description="Stores stats about read manga.")

WholeNumber = conint(gt=0)


class ErrorModel(BaseModel):
    """
    An error model.
    """

    detail: str


class StatsInput(BaseModel):
    manga_id: UUID
    chapter_num: float
    pages: WholeNumber
    bytes: WholeNumber


class StatsChapter(BaseModel):
    id: WholeNumber
    pages: WholeNumber
    bytes: WholeNumber
    read_on: datetime


class StatsOutput(BaseModel):
    manga_id: UUID
    chapters: Dict[float, StatsChapter]


class AllStats(BaseModel):
    stats: Dict[UUID, StatsOutput]


@app.on_event("startup")
async def startup_event():
    await init()


@app.post("/stats", status_code=201, response_model=StatsChapter)
async def post_stats(stats: StatsInput):
    model = StatsEntry(
        manga_uuid=stats.manga_id,
        chapter_num=stats.chapter_num,
        pages=stats.pages,
        bytes=stats.bytes,
    )
    await model.save()
    return StatsChapter(
        id=model.id, pages=model.pages, bytes=model.bytes, read_on=model.created_on
    )


@app.get(
    "/stats/{manga_id}",
    response_model=StatsOutput,
    responses={404: {"model": ErrorModel}},
)
async def get_stats(manga_id: UUID):
    entries = await StatsEntry.filter(manga_uuid=manga_id).order_by("chapter_num").all()
    if not entries:
        raise HTTPException(status_code=404, detail="Manga not found.")
    chapters = {}
    for entry in entries:
        chapters[entry.chapter_num] = StatsChapter(
            id=entry.id, pages=entry.pages, bytes=entry.bytes, read_on=entry.created_on
        )
    return StatsOutput(manga_id=manga_id, chapters=chapters)


@app.get("/stats", response_model=AllStats)
async def get_all_stats():
    entries = await StatsEntry.all()
    stats = {}
    for entry in entries:
        if entry.manga_uuid not in stats:
            stats[entry.manga_uuid] = StatsOutput(
                manga_id=entry.manga_uuid, chapters={}
            )
        stats[entry.manga_uuid].chapters[entry.chapter_num] = StatsChapter(
            id=entry.id, pages=entry.pages, bytes=entry.bytes, read_on=entry.created_on
        )
    return AllStats(stats=stats)
