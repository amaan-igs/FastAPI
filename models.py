from pydantic import BaseModel, EmailStr

class User(BaseModel):
    username: str
    email: EmailStr
    password: str

class Book(BaseModel):
    title: str
    author: str
    genre: str
    price: float