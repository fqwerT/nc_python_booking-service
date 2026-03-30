from sqlalchemy import Column, DateTime, Integer, String, Sequence,VARCHAR,ForeignKey
from sqlalchemy.orm import declarative_base
from models.base import Base


class Booking(Base):
    __tablename__ = "bookings"
    id = Column(String(228), primary_key=True, nullable=False, index=True)
    room_id = Column(String(228), ForeignKey('rooms.id'), nullable=False, index=True)
    guest_name = Column(String, nullable=False)
    check_in = Column(DateTime, nullable=False, index=True)
    check_out = Column(DateTime, nullable=False, index=True)
    user_id = Column(String(228), nullable=False, index=True)
    status = Column(String, nullable=False, default="confirmed")