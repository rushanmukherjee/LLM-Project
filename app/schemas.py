from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

class GroceryItemBase(BaseModel):
    name: str
    quantity: int
    unit: str
    is_essential: bool = False

class GroceryItemCreate(GroceryItemBase):
    pass

class GroceryItem(GroceryItemBase):
    id: int
    is_completed: bool
    grocery_list_id: int

    class Config:
        from_attributes = True

class GroceryListBase(BaseModel):
    title: str

class GroceryListCreate(GroceryListBase):
    pass

class GroceryList(GroceryListBase):
    id: int
    owner_id: int
    created_at: datetime
    items: List[GroceryItem] = []

    class Config:
        from_attributes = True

class ReminderBase(BaseModel):
    reminder_date: datetime
    is_active: bool = True

class ReminderCreate(ReminderBase):
    item_id: int

class Reminder(ReminderBase):
    id: int
    user_id: int
    item_id: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None 