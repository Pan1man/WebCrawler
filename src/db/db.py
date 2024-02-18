from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DATABASE_URL = "postgresql+asyncpg://postgres:sa@localhost/gruzdle_db"

engine = create_async_engine(
    DATABASE_URL
)

new_session = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()
