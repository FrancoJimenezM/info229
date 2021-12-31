from typing import List, Optional

from pydantic import BaseModel


class NewsBase(BaseModel):
    title: str
    description: Optional[str] = None


class NewsCreate(NewsBase):
    pass


class News(NewsBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class CategoryAssign(NewsBase):
    category: str


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: List[News] = []

    class Config:
        orm_mode = True

