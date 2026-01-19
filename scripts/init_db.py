import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.infrastructure.database.session import db_manager


async def init_database():
    try:
        await db_manager.create_tables()
        async with db_manager.engine.connect() as conn:
            await conn.execute("SELECT 1")
        
    except Exception as e:
        print(f"Failed to initialize database: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(init_database())