from pydantic import BaseModel
from typing import Optional


class UserCreate(BaseModel):
    phone: str
    full_name: Optional[str] = None
    tg_id: Optional[str] = None
    vk_id: Optional[str] = None
    wa_id: Optional[str] = None


class TicketCreate(BaseModel):
    user_id: str
    messenger: str
    problem_type: str
    status: str
    start_datetime: Optional[str] = None
    end_datetime: Optional[str] = None
    text: Optional[str] = None # for messages


class ServiceAdd(BaseModel):
    user_id: str
    service_type: str
    service_name: str
    price: Optional[float] = None