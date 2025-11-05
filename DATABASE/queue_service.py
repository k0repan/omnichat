import aio_pika
import json
from typing import Dict, Any
import asyncio


class QueueService:
    def __init__(self):
        self.conn = None
        self.channel = None


    async def connect(self, rabbitmq_url: str = "amqp://guest:guest@localhost/"):
        self.conn = await aio_pika.connect_robust(rabbitmq_url)
        self.channel = await self.conn.channel()

        await self.channel.declare_queue("ticket_created", durable=True)
        await self.channel.declare_queue("ticket_assigned", durable=True)
        

    async def publish_ticket_created(self, ticket_data: Dict[str, Any]):
        message = aio_pika.Message(
            body=json.dumps(ticket_data).encode(),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT
        )
        await self.channel.default_exchange.publish(
            message, routing_key="ticket_created"
        )


    async def publish_ticket_assigned(self, ticket_data: Dict[str, Any]):
        message = aio_pika.Message(
            body=json.dumps(ticket_data).encode(),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT
        )
        await self.channel.default_exchange.publish(
            message, routing_key="ticket_assigned"
        )


    async def consume_ticket_created(self, callback):
        queue = await self.channel.declare_queue("ticket_created", durable=True)
        await queue.consume(callback)

    
    async def close(self):
        if self.conn:
            await self.conn.close()


queue_service = QueueService()