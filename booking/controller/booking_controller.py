from fastapi import APIRouter, Depends
from auth.dependencies import get_current_user
from auth.model.auth_model import User
from booking.schemas.booking_schemas import BookingCreate, BookingResponse
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