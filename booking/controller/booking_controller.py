from fastapi import APIRouter, Depends, Query, HTTPException
from auth.dependencies import get_current_user
from auth.model.auth_model import User
from booking.schemas.booking_schemas import BookingCreate, BookingResponse, BookingUpdate
from booking.service.booking_service import BookingService
from booking.repository.booking_repository import BookingRepository
from db_init import get_db
from sqlalchemy.orm import Session

router = APIRouter()

def get_booking_repository(db_session: Session = Depends(get_db)) -> BookingRepository:
    return BookingRepository(db_session)


def get_booking_service(
    booking_repository: BookingRepository = Depends(get_booking_repository),
) -> BookingService:
    return BookingService(booking_repository)


@router.get("/", response_model=list[BookingResponse], summary="Список всех бронирований")
def get_bookings(booking_service: BookingService = Depends(get_booking_service)):
    return booking_service.get_bookings()

@router.get("/by_room", response_model=list[BookingResponse], summary="Получить бронирование по ID комнаты")
def get_bookings( room_id: str = Query(..., description="ID комнаты для поиска бронирований"),
    booking_service: BookingService = Depends(get_booking_service)):
    return booking_service.get_booking_by_room_id(room_id)

@router.get("/by_user", response_model=list[BookingResponse], summary="Получить бронирование по ID пользователя")
def get_bookings( user_id: str = Query(..., description="ID пользователя создавшего бронь"),
    booking_service: BookingService = Depends(get_booking_service)):
    return booking_service.get_booking_by_user_id(user_id)


@router.delete("/delete",response_model=bool, summary="Получить бронирование по ID комнаты")
def deleteBooking( id: str = Query(..., description="ID бронирования для удаления"),
    booking_service: BookingService = Depends(get_booking_service)):
    return booking_service.deleteBooking(id)

@router.post(
    "/",
    response_model=BookingResponse,
    summary="Создание события бронирования переговорной комнаты",
)
def create_booking(
    booking_in: BookingCreate,
    booking_service: BookingService = Depends(get_booking_service),
    current_user: User = Depends(get_current_user),
):
    return booking_service.create_booking(booking_in, current_user)



@router.patch(
    "/update_booking",
    response_model=BookingResponse,
    summary="Обновление брони",
)
def update_booking(
    booking_new_data: BookingUpdate,
    booking_service: BookingService = Depends(get_booking_service),
):

    return booking_service.update_booking(booking_new_data)