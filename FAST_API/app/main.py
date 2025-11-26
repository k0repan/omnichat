import sys
sys.path.insert(0, "..")
from fastapi import HTTPException, BackgroundTasks
from datetime import datetime
from fastapi import FastAPI
from .models import *
# from DATABASE.db_class_sql import db
# from DATABASE.queue_service import queue_service


app = FastAPI(title="Omnichat Support API")


@app.post("/api/users/register")
async def register_user(user_data: UserCreate):
    user = await db.create_or_update_user(
        phone=user_data.phone,
        full_name=user_data.full_name,
        tg_id=user_data.tg_id,
        vk_id=user_data.vk_id,
        wa_id=user_data.wa_id
    )
    if not user:
        return {"status": "failed", "user": user}
    return {"status": "success", "user": user}


@app.get("/api/users/{phone}")
async def get_user(phone: str):
    user = await db.get_user_by_phone(phone)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    services = db.get_user_service(user["id"])
    return {"user": user, "services": services}


@app.post("/api/tickets/create")
async def create_ticket(ticket_data: TicketCreate, background_tasks: BackgroundTasks):
    user = await db.get_user_by_id(ticket_data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    ticket = await db.create_ticket(
        user_id=ticket_data.user_id,
        messenger=ticket_data.messenger,
        problem_type=ticket_data.problem_type,
        status=ticket_data.status,
        text=ticket_data.text,
        start_datetime=ticket_data.start_datetime
    )

    background_tasks.add_task(
        queue_service.publish_ticket_created,
        {
            "id": ticket["id"],
            "user_id": ticket_data.user_id,
            "messenger": ticket_data.messenger,
            "problem_type": ticket_data.problem_type,
            "status": ticket_data.status,
            "start_datetime": str(datetime.now())
        }
    )

    return {"status": "success", "ticket": ticket}
    

@app.get("/api/tickets/user/{phone}")
async def get_user_tickets(phone: str, limit: int = 10):
    user = await db.get_user_by_phone(phone)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    tickets = db.get_user_tickets(user["id"], limit)
    return {"tickets": tickets}


@app.get("/api/tickets/{ticket_id}")
async def get_ticket(ticket_id: int):
    ticket = await db.get_ticket_by_id(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    messages = await db.get_ticket_messages(ticket["id"])

    return {"ticket": ticket, "messages": messages}


@app.post("/api/tickets/{ticket_id}/close")
async def close_ticket(ticket_id: int):
    ticket = await db.get_ticket_by_id(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    await db.update_ticket(ticket_id, status="closed")


@app.post("/api/services/add")
async def add_service(service_data: ServiceAdd):
    user = await db.get_user_by_id(service_data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    service = await db.add_user_service(
        user_id=service_data.user_id,
        service_type=service_data.service_type,
        service_name=service_data.service_name,
        price=service_data.price
    )

    return {"status": "success", "service": service}
