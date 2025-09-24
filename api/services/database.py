from prisma import Prisma
from typing import Optional, List
import asyncio

class DatabaseService:
    def __init__(self):
        self.prisma = Prisma()
    
    async def connect(self):
        await self.prisma.connect()
    
    async def disconnect(self):
        await self.prisma.disconnect()

# Инициализация базы данных
db_service = DatabaseService()

async def get_db():
    if not db_service.prisma.is_connected():
        await db_service.connect()
    return db_service.prisma