from fastapi import APIRouter
from typing import List

from src.models.web_pages import WebPage
from src.utils.repository import WebPageRepository

router = APIRouter(
    prefix="/pages"
)

@router.get("")
async def get_pages():
    pages = await WebPageRepository.get_all()

    return {"pages": pages}