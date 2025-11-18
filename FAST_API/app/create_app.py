import sys
sys.path.insert(0, "..")
import os
from fastapi import FastAPI
from contextlib import asynccontextmanager
from models import *
from DATABASE.db_class import db
from DATABASE.queue_service import queue_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.init_db()
    await queue_service.connect()
    yield
    await queue_service.close()

app = FastAPI(title="Omnichat Support API", lifespan=lifespan)
