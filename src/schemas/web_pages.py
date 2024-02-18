from pydantic import BaseModel
from datetime import date


class WebPageBase(BaseModel):
    url: str
    title: str
    description: str
    last_time_visited: date
