import asyncio
import asyncpg
from datetime import datetime
from typing import List, Dict, Any, Optional
import json


class Database:
    def __init__(self):
        self.pool = None

    
    async def init_db(self):
        self.pool = await asyncpg.create_pool(
            "postgresql://user:pass@localhost/omnichat_support",
            min_size=5,
            max_size=20
        )
        await self.create_tables()


    async def create_tables(self):
        async with self.pool.acquire() as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS tickets (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id),
                    messenger VARCHAR(20) NOT NULL,
                    problem_type VARCHAR(50) NOT NULL,
                    status VARCHAR(20) DEFAULT 'open',
                    start_datetime TIMESTAMP DEFAULT NOW(),
                    end_datetime TIMESTAMP DEFAULT NOW()
                )
            """)

            await conn.execute("""
                CREATE TABLE IF NOT EXISTS ticket_messages (
                    id SERIAL PRIMARY KEY,
                    ticket_id INTEGER REFERENCES tickets(id),
                    messenger VARCHAR(20) NOT NULL REFERENCES tickets(messenger),
                    send_datetime TIMESTAMP DEFAULT NOW(),
                    text VARCHAR(256)
                )
            """)

            await conn.execute("""
                CREATE TABLE IF NOT EXISTS user_services (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id),
                    service_type VARCHAR(50) NOT NULL,
                    service_name VARCHAR(100) NOT NULL,
                    status VARCHAR(20) DEFAULT 'active',
                    price DECIMAL(10, 2),
                    activate_datetime TIMESTAMP DEFAULT NOW(),
                    create_datetime TIMESTAMP DEFAULT NOW()
                )
            """)

            await conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    phone VARCHAR(20) UNIQUE NOT NULL,
                    full_name VARCHAR(100),
                    tg_id VARCHAR(50),
                    vk_id VARCHAR(50),
                    wa_id VARCHAR(50)
                )
            """)

            await conn.execute("CREATE INDEX IF NOT EXISTS idx_user_phone ON users(phone)")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_ticket_status ON tickets(status)")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_ticket_user_id ON tickets(user_id)")
            

    async def create_or_update_user(self, phone: str, full_name: str, tg_id: str, vk_id: str, wa_id: str):
        async with self.pool.acquire() as conn:
            user = await conn.fetchrow("""
                INSERT INTO users (phone, full_name, tg_id, vk_id, wa_id)
                    VALUES ($1, $2, $3, $4, $5)
                    ON CONFLICT (phone)
                    DO UPDATE SET
                        full_name = COALESCE(EXCLUDED.full_name, users.full_name),
                        tg_id = COALESCE(EXCLUDED.tg_id, users.tg_id),
                        vk_id = COALESCE(EXCLUDED.vk_id, users.vk_id),
                        wa_id = COALESCE(EXCLUDED.wa_id, users.wa_id)
            """, phone, full_name, tg_id, vk_id, wa_id)

            return dict(user) if user else None


    async def create_ticket(self, user_id: int, messenger: str, problem_type: str, text: str, status: str = "active"):
        async with self.pool.acquire() as conn:
            ticket = await conn.fetchrow("""
                INSERT INTO tickets (user_id, messenger, problem_type, status)
                    VALUES ($1, $2, $3, $4)
                    RETURNING *
            """, user_id, messenger, problem_type, status)

            await self.add_ticket_message(ticket["id"], messenger, text) 

            return dict(ticket)
        
    
    async def update_ticket(self, ticket_id: int, status: str):
        async with self.pool.acquire() as conn:
            await conn.execute("""
                UPDATE tickets
                    SET status = $1, end_datetime = NOW()
                    WHERE id = $2
            """, status, ticket_id)
    

    async def add_user_service(self, user_id: int, service_type: str, service_name: str, price: float = None):
        async with self.pool.acquire() as conn:
            service = await conn.fetchrow('''
                INSERT INTO user_services (user_id, service_type, service_name, price)
                VALUES ($1, $2, $3, $4)
                RETURNING *
            ''', user_id, service_type, service_name, price)
            return dict(service)


    async def add_ticket_message(self, ticket_id: int, messenger: str, text: str):
        async with self.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO ticket_messages (ticket_id, messenger, text)
                    VALUES ($1, $2, $3)
            """, ticket_id, messenger, text)

        
    async def get_ticket_by_id(self, ticket_id: int):
        async with self.pool.acquire() as conn:
            ticket = await conn.execute("""
                SELECT * FROM tickets WHERE id = $1
            """, ticket_id)
            return dict(ticket) if ticket else None


    async def get_ticket_messages(self, ticket_id: int):
        async with self.pool.acquire() as conn:
            messages = await conn.execute("""
                SELECT * FROM ticket_messages WHERE ticket_id = $1 ORDER BY send_datetime
            """, ticket_id)
            return [dict(message) for message in messages]


    async def get_user_by_phone(self, phone: str):
        async with self.pool.acquire() as conn:
            user = await conn.execute("""
                SELECT * FROM users WHERE phone = $1
            """, phone)
            return dict(user) if user else None
        

    async def get_user_by_id(self, user_id: int):
        async with self.pool.acquire() as conn:
            user = await conn.execute("""
                SELECT * FROM users WHERE id = $1
            """, user_id)
            return dict(user) if user else None


    async def get_user_service(self, user_id: int):
        async with self.pool.acquire() as conn:
            services = await conn.fetch("""
                SELECT * FROM user_services
                    WHERE user_id = $1 AND status = 'active'
                    ORDER BY service_type
            """, user_id)
            return [dict(service) for service in services]
        
    async def get_user_tickets(self, user_id: int, limit: int = 10):
        async with self.pool.acquire() as conn:
            tickets = await conn.fetch('''
                SELECT * FROM tickets 
                WHERE user_id = $1 
                ORDER BY start_datetime DESC 
                LIMIT $2
            ''', user_id, limit)
            return [dict(ticket) for ticket in tickets]
        

db = Database()