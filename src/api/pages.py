import os

from fastapi import APIRouter, Depends, Request, Form
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.templating import Jinja2Templates

from src.db.db import get_async_session
from src.models.pages import Page
from src.schemas.pages import PageBase
from pathlib import Path

router = APIRouter()

templates_dir = Path(__file__).resolve().parents[1] / "templates"

templates = Jinja2Templates(directory=str(templates_dir))

@router.get("/")
async def get_main_template(request: Request):
    return templates.TemplateResponse("main_template.html", {"request": request})


@router.post("/submit")
async def submit_form(input_text: str = Form(...)):
    return input_text

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
