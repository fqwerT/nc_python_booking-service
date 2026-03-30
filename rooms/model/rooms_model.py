from sqlalchemy import Column, DateTime, Integer, String, Sequence,JSON
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from booking.model.booking_model import Booking
from models.base import Base


class Room(Base):
    __tablename__ = "rooms"
    id = Column(String(228), primary_key=True, nullable=False, index=True)
    name = Column(String, nullable=False)