from pydantic import BaseModel
from datetime import date

from typing_extensions import Union, List


class PageBase(BaseModel):
    url: str
    title: str
    description: str
    tags: Union[str, List[str]]
    last_time_visited: date
