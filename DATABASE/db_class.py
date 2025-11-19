from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from config import get_db_url

DB_URL = get_db_url()

engine = create_async_engine(DB_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Database:
    def __init__(self, db_url: str = DB_URL):
        pass