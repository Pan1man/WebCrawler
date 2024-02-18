from sqlalchemy import select
from src.db.db import new_session
from src.models.web_pages import WebPage


class WebPageRepository:
    @classmethod
    async def get_all(cls):
        async with new_session() as session:
            query = select(WebPage)
            result = await session.execute(query)
            web_pages_models = result.scalars().all()
            return web_pages_models
