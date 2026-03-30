from pydantic import BaseModel, field_validator, ValidationInfo
from datetime import datetime
from typing import Optional

class BookingBase(BaseModel):
    guest_name: str
    room_id: str
    check_in: datetime
    check_out: datetime


class BookingCreate(BookingBase):
    pass


class BookingResponse(BookingBase):
    id: str
    status: str

    class Config:
        from_attributes = True

class BookingUpdate(BaseModel):
    id: str 
    guest_name: Optional[str] = None
    room_id: Optional[str] = None
    check_in: Optional[datetime] = None
    check_out: Optional[datetime] = None
    @field_validator('check_out')
    @classmethod
    def validate_check_out(cls, v: Optional[datetime], info: ValidationInfo) -> Optional[datetime]:
        if v is not None:
            check_in = info.data.get('check_in')
            if check_in is not None:
                if v <= check_in:
                    raise ValueError('check_out must be after check_in')
        return v
    
    @field_validator('check_in')
    @classmethod
    def validate_check_in(cls, v: Optional[datetime], info: ValidationInfo) -> Optional[datetime]:
        if v is not None:
            check_out = info.data.get('check_out')
            if check_out is not None:
                if check_out <= v:
                    raise ValueError('check_out must be after check_in')
        return v