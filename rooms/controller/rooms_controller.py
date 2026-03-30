from fastapi import APIRouter, Depends, Query
from auth.dependencies import get_current_user
from auth.model.auth_model import User
from rooms.schemas.rooms_schemas import RoomsCreate, RoomsResponse,RoomUpdate
from rooms.service.rooms_service import RoomsService
from rooms.repository.rooms_repository import RoomsRepository
from db_init import get_db
from sqlalchemy.orm import Session

router = APIRouter()

def get_rooms_repository(db_session: Session = Depends(get_db)) -> RoomsRepository:
    return RoomsRepository(db_session)


def get_rooms_service(db: Session = Depends(get_db)) -> RoomsService:
    rooms_repository = RoomsRepository(db)
    return RoomsService(rooms_repository)

@router.get("/rooms", response_model=list[RoomsResponse], summary="Список всех комнат")
def get_rooms(
    rooms_service: RoomsService = Depends(get_rooms_service)
):
    return rooms_service.get_all_rooms()


@router.get("/room_by_id", response_model=list[RoomsResponse], summary="Список всех комнат")
def get_rooms(
    rooms_service: RoomsService = Depends(get_rooms_service),
    id:str = Query(...,summary="ID комнаты")
):
    return rooms_service.get_room_by_ID(id)

@router.patch("/update", response_model=RoomsResponse, summary="Обновление комнаты по ID")
def update_room(
    id: str = Query(..., summary="ID комнаты"),
    room_update: RoomUpdate = None,  
    rooms_service: RoomsService = Depends(get_rooms_service),
):
    return rooms_service.update_room_by_id(room_update, id)

@router.delete("/delete",response_model=bool,summary="Удвление переговорной комнаты по ID")
def delete_rooms(
    rooms_service: RoomsService = Depends(get_rooms_service),
    id:str = Query(...,description="ID бронирования для удаления")
):
    return rooms_service.delete_room_by_ID(id)

@router.post(
    "/rooms",
    response_model=RoomsResponse,
    summary="Создание события бронирования переговорной комнаты",
)
def create_rooms(
    rooms_in: RoomsCreate,
    rooms_service: RoomsService = Depends(get_rooms_service),
  
):
    return rooms_service.create_room(rooms_in)