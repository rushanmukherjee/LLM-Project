from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    
    grocery_lists = relationship("GroceryList", back_populates="owner")
    reminders = relationship("Reminder", back_populates="user")

class GroceryList(Base):
    __tablename__ = "grocery_lists"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    owner = relationship("User", back_populates="grocery_lists")
    items = relationship("GroceryItem", back_populates="grocery_list")

class GroceryItem(Base):
    __tablename__ = "grocery_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    quantity = Column(Integer)
    unit = Column(String)
    is_essential = Column(Boolean, default=False)
    is_completed = Column(Boolean, default=False)
    grocery_list_id = Column(Integer, ForeignKey("grocery_lists.id"))
    
    grocery_list = relationship("GroceryList", back_populates="items")
    reminder = relationship("Reminder", back_populates="item", uselist=False)

class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("grocery_items.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    reminder_date = Column(DateTime)
    is_active = Column(Boolean, default=True)
    
    item = relationship("GroceryItem", back_populates="reminder")
    user = relationship("User", back_populates="reminders") 