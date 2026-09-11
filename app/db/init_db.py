import asyncio
import asyncpg
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.core.config import settings

async def init_db():
    try:
        conn = await asyncpg.connect(settings.DATABASE_URL)
        
        with open("app/db/tables.sql", "r") as f:
            sql_queries = f.read()
        
        await conn.execute(sql_queries)
        
        await conn.close()
    except Exception as e:
        print(f"Something went wrong: {e}")

if __name__ == "__main__":
    asyncio.run(init_db())
    