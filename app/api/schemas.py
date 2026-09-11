from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class ProductCreate(BaseModel):
    name: str
    price: float
    stock_quantity: int

class ProductResponse(BaseModel):
    id: str
    name: str
    price: float
    stock_quantity: int
