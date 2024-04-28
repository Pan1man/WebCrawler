import os

from fastapi import APIRouter, Depends, Request, Form
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.templating import Jinja2Templates

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
async def start_parsing(frontier: Frontier = Depends(url_frontier)):
    global current_parsing_task

    if current_parsing_task and not current_parsing_task.done():
        return "Парсинг уже запущен. Невозможно запустить парсинг повторно."

    current_parsing_task = asyncio.create_task(Fetcher.fetch(frontier))
    return "Парсинг начат."


@router.get("/end_parsing")
async def end_parsing():
    global current_parsing_task

    if current_parsing_task and not current_parsing_task.done():
        current_parsing_task.cancel()
        return "Парсинг остановлен."

    return "Парсинг не запущен. Нет действий для завершения."



@router.get("/pages")
async def get_pages(session: AsyncSession = Depends(get_async_session)):
    query = select(Page)
    pages = await session.execute(query)
    result = pages.scalars().all()
    return result


@router.put("/add_page")
async def add_page(page: PageBase, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(Page).values(**page.dict())
    await session.execute(stmt)
    await session.commit()

