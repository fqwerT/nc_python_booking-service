from pydantic import BaseModel
from datetime import datetime


class BookingBase(BaseModel):
    guest_name: str
    room_number: int
    check_in: datetime
    check_out: datetime


class BookingCreate(BookingBase):
    pass


class BookingResponse(BookingBase):
    id: str
    status: str

    class Config:
        from_attributes = True