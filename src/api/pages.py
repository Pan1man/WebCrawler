import os

from fastapi import APIRouter, Depends, Request, Form
from sqlalchemy import select, insert, func, String, or_
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.templating import Jinja2Templates
from typing_extensions import List, Union

from src.db.db import get_async_session
from src.models.pages import Page
from src.schemas.pages import PageBase
from pathlib import Path


from src.urlfrontier import url_frontier
from src.urlfrontier import Frontier
from src.parser import Fetcher

import asyncio

router = APIRouter()

templates_dir = Path(__file__).resolve().parents[1] / "templates"

templates = Jinja2Templates(directory=str(templates_dir))

current_parsing_task = None
@router.get("/")
async def get_main_template(request: Request):
    return templates.TemplateResponse("main_template.html", {"request": request})


@router.post("/submit")
async def submit_form(request: Request, url: str = Form(...), frontier: Frontier = Depends(url_frontier)):
    try:
        frontier.add_url(url)
        return templates.TemplateResponse("main_template.html", {"request": request})
    except Exception as e:
        return "Ошибка"


@router.get("/start_parsing")
async def start_parsing(frontier: Frontier = Depends(url_frontier), session: AsyncSession = Depends(get_async_session)):
    global current_parsing_task

    if current_parsing_task and not current_parsing_task.done():
        return "Парсинг уже запущен. Невозможно запустить парсинг повторно."

    current_parsing_task = asyncio.create_task(Fetcher.fetch(frontier, session))
    return "Парсинг начат."


@router.get("/end_parsing")
async def end_parsing(session: AsyncSession = Depends(get_async_session)):
    global current_parsing_task

    if current_parsing_task and not current_parsing_task.done():
        current_parsing_task.cancel()
        await session.close()
        return "Парсинг остановлен."

    return "Парсинг не запущен. Нет действий для завершения."



@router.get("/pages")
async def get_all_pages(session: AsyncSession = Depends(get_async_session)):
    query = select(Page)
    pages = await session.execute(query)
    result = pages.scalars().all()
    return result


@router.put("/add_page")
async def add_page(page: PageBase, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(Page).values(**page.dict())
    await session.execute(stmt)
    await session.commit()




@router.get("/api/get_pages/{key_words}")
async def get_pages(key_words: str, session: AsyncSession = Depends(get_async_session)):
    key_words_list = key_words.split()
    first_word_condition = [
        func.split_part(Page.title, ' ', 1).ilike(f"{word}%") for word in key_words_list
    ]

    query = select(Page).filter(
        or_(*first_word_condition),
        func.array_length(Page.tags, 1) >= 3,
    )


    pages = await session.execute(query)
    result = pages.scalars().all()


    if not result:
        query = select(Page).filter(
            func.array_length(Page.tags, 1) >= 3,
            *[
                func.cast(Page.tags, String).ilike(f"%{word}%") for word in key_words_list
            ]
        )
        pages = await session.execute(query)
        result = pages.scalars().all()

    return result

