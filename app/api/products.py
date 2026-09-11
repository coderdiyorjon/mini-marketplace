import json
from fastapi import APIRouter, HTTPException, Depends, status
from app.api.schemas import ProductCreate, ProductResponse
from app.db.database import Database
from app.db.redis import RedisCache
from app.api.dedps import get_current_user_id

router = APIRouter(prefix="/products", tags=["products"])

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate, user_id: str = Depends(get_current_user_id)):
    query = "INSERT INTO products (name, price, stock_quantity) VALUES ($1, $2, $3) RETURNING id, name, price, stock_quantity"
    result = await Database.fetch(query, product.name, product.price, product.stock_quantity)
    
    product_dict = dict(result[0])
    
    product_dict['id'] = str(product_dict['id'])
    
    return product_dict

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: str):
    cache_key = f"product:{product_id}"
    
    cached_data = await RedisCache.get(cache_key)
    if cached_data:
        print("From Redis Cache")
        return json.loads(cached_data)
        
    print("From Database")
    query = "SELECT id, name, price, stock_quantity FROM products WHERE id = $1"
    result = await Database.fetch(query, product_id)
    
    if not result:
        raise HTTPException(status_code=404, detail="Product not found")
        
    product_dict = dict(result[0])
    
    product_dict['id'] = str(product_dict['id'])
    product_dict['price'] = float(product_dict['price'])
    
    await RedisCache.set(cache_key, json.dumps(product_dict), ex=3600)
    
    return product_dict