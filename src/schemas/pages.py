from pydantic import BaseModel
from datetime import date


class PageBase(BaseModel):
    url: str
    title: str
    description: str
    last_time_visited: date
