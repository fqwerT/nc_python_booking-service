from pydantic import BaseModel
from datetime import datetime


class RoomsBase(BaseModel):
    name: str


class RoomsCreate(RoomsBase):
    pass


class RoomsResponse(RoomsBase):
    id: str
    name: str

    class Config:
        from_attributes = True

        
class RoomUpdate(RoomsBase):
    pass
