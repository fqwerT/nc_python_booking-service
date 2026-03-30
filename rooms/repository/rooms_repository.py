from datetime import datetime

from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from rooms.model.rooms_model  import Room


class RoomsRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_all_rooms(self) -> list[Room]:
        return self.db_session.query(Room).all()
    
    def get_room_by_ID(self,id:str = "") -> list[Room]:
        return self.db_session.query(Room).filter(Room.id == id)
    
    def delete_room_by_ID(self,id) -> bool:
        room_to_delete = self.db_session.query(Room).filter(Room.id == id).one()
        if room_to_delete:
           self.db_session.delete(room_to_delete)
           self.db_session.commit()
        
           return True
        else:
           return False 

    def create_room(
        self,
        name:str,
        unique_id:str
    ) -> Room:
        room = Room(
            name=name,
            id=unique_id
        )
        self.db_session.add(room)
        self.db_session.commit()
        self.db_session.refresh(room)
        
        return room
    
    def update_room_by_id(self,room_update, id:str = "",) -> Room:    
        room_to_update = self.db_session.query(Room).filter(Room.id == id).first()
        if not room_to_update:
            raise ValueError(f"Booking with id {room_to_update.id} not found")
        else:
            setattr(room_to_update, "name", room_update.name)
            self.db_session.commit()
            self.db_session.refresh(room_to_update)
    
            return room_to_update


