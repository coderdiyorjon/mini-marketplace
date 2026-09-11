from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.orders import router as orders_router
from app.api.products import router as products_router
from app.db.database import Database
from app.db.redis import RedisCache


@asynccontextmanager
async def lifespan(app: FastAPI):
    await Database.connect()
    await RedisCache.connect()
    yield
    await Database.disconnect()
    await RedisCache.disconect()


app = FastAPI(title="Mini Marketplace API", lifespan=lifespan)

app.include_router(auth_router)
app.include_router(products_router)
app.include_router(orders_router)


@app.get("/health")
async def health_check():
    return {"status": "Databse connects automaticaly"}
