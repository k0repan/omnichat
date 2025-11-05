import sys
sys.path.insert(0, "..")
import requests
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from DATABASE.db_class import db


db_router = Router()


