import datetime

from sqlalchemy import Column, VARCHAR, TEXT, DATE, MetaData
from sqlalchemy.orm import declarative_base


metadata = MetaData()
Base = declarative_base(metadata=metadata)

class Page(Base):
    __tablename__ = "pages"
    url = Column(VARCHAR, primary_key=True)
    title = Column(VARCHAR)
    description = Column(TEXT)
    last_time_visited = Column(DATE, nullable=False, default=datetime.date)
