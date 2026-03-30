from datetime import timedelta
from fastapi import HTTPException, status
from rooms.repository.rooms_repository import RoomsRepository
import uuid
from rooms.schemas.rooms_schemas import RoomsResponse,RoomsCreate,RoomUpdate
from rooms.model.rooms_model import Room
class RoomsService:
      def __init__(self, rooms_repository: RoomsRepository):
        self.rooms_repository = rooms_repository

      def get_all_rooms(self) -> list[RoomsResponse]:
        rooms = self.rooms_repository.get_all_rooms()
        return [RoomsResponse.model_validate(b) for b in rooms]
      
      def delete_room_by_ID(self,id:str) -> bool:
        return self.rooms_repository.delete_room_by_ID(id)

      def create_room(self,roomData:RoomsCreate):
        name = roomData.name
        unique_id = str(uuid.uuid4())
        new_room = self.rooms_repository.create_room(name,unique_id)
        return new_room
      
      def get_room_by_ID(self,id:str =""):
        foundedRoom = self.rooms_repository.get_room_by_ID(id)
        return foundedRoom
      
      def update_room_by_id(self,room_update:RoomUpdate,id:str = "",) -> Room:
        return self.rooms_repository.update_room_by_id(room_update,id)
          
