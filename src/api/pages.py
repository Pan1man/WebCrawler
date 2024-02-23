
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import List

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

