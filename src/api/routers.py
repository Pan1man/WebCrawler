from fastapi import APIRouter
from src.utils.repository import WebPageRepository

router = APIRouter(
    prefix="/pages"
)

@router.get("")
async def get_pages():
    #import pdb; pdb.set_trace()
    pages = await WebPageRepository.get_all()
    return {"pages": pages}