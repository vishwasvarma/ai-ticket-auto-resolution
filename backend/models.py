from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP
from backend.database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True} 

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(String)

class Ticket(Base):
    __tablename__ = "tickets"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    ticket_number = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    response = Column(Text)
    category = Column(String)
    status = Column(String, default="open")
    type = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)