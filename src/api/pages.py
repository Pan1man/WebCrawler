from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.db import get_async_session
from src.models.pages import Page
from src.schemas.pages import PageBase

router = APIRouter()


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
