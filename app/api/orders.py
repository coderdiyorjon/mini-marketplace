from fastapi import APIRouter, HTTPException, Depends, Header, status
from app.api.schemas import OrderCreate
from app.db.database import Database
from app.api.dedps import get_current_user_id
import asyncpg

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_order(
    order: OrderCreate,
    idempotency_key: str = Header(...),
    user_id: str = Depends(get_current_user_id)
):
    if Database.pool is None:
        raise HTTPException(status_code=500, detail="Database not connected")

    async with Database.pool.acquire() as conn:
        try:
            async with conn.transaction():
                try:
                    order_query = """
                        INSERT INTO orders (user_id, idempotency_key, status)
                        VALUES ($1, $2, 'pending') RETURNING id
                    """
                    order_id = await conn.fetchval(order_query, user_id, idempotency_key)
                except asyncpg.exceptions.UniqueViolationError:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="Order already created with this key"
                    )

                for item in order.items:
                    update_stock_query = "UPDATE products SET stock_quantity = stock_quantity - $1 WHERE id = $2 AND stock_quantity >= $1 RETURNING price"
                    price = await conn.fetchval(update_stock_query, item.quantity, item.product_id)

                    if price is None:
                        raise HTTPException(
                            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=f"Product {item.product_id} not enough or not found"
                        )

                    insert_item_query = "INSERT INTO order_items (order_id, product_id, quantity, price) VALUES ($1, $2, $3, $4)"
                    await conn.execute(insert_item_query, order_id, item.product_id, item.quantity, price)

                return {"message": "Successfully created", "order_id": str(order_id)}

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))