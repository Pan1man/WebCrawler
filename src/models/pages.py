import datetime

from sqlalchemy import Column, VARCHAR, TEXT, DATE, MetaData, ARRAY
from sqlalchemy.orm import declarative_base


metadata = MetaData()
Base = declarative_base(metadata=metadata)

class Page(Base):
    __tablename__ = "pages"
    url = Column(VARCHAR, primary_key=True)
    title = Column(VARCHAR)
    description = Column(TEXT)
    tags = Column(ARRAY(VARCHAR))
    last_time_visited = Column(DATE, nullable=False, default=datetime.date)

    def __init__(self, url, title, description, tags, last_time_visited=datetime.date.today()):
        self.url = url
        self.title = title
        self.description = description
        self.tags = tags
        self.last_time_visited = last_time_visited
