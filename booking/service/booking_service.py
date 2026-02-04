from datetime import timedelta
from fastapi import HTTPException, status
from auth.model.auth_model import User
from booking.repository.booking_repository import BookingRepository
from booking.schemas.booking_schemas import BookingCreate, BookingResponse
import uuid

class BookingService:

    MIN_DURATION = timedelta(minutes=30)
    MAX_DURATION = timedelta(hours=24)

    def __init__(self, booking_repository: BookingRepository):
        self.booking_repository = booking_repository

    def get_bookings(self) -> list[BookingResponse]:
        bookings = self.booking_repository.get_all_bookings()
        return [BookingResponse.model_validate(b) for b in bookings]

    def create_booking(
        self, booking_in: BookingCreate, current_user: User
    ) -> BookingResponse:

        check_in = booking_in.check_in
        check_out = booking_in.check_out
        
        if check_in >= check_out:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Время начала должно быть раньше времени окончания",
            )

        duration = check_out - check_in
        
        if duration < self.MIN_DURATION:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Минимальный интервал бронирования — {self.MIN_DURATION}",
            )
        if duration > self.MAX_DURATION:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Максимальный интервал бронирования — {self.MAX_DURATION}",
            )

        overlapping = self.booking_repository.get_overlapping_bookings(
            room_number=booking_in.room_number,
            start=check_in,
            end=check_out,
        )

        if overlapping:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="В указанный интервал комната уже забронирована",
            )
            
        unique_id = str(uuid.uuid4())
        booking = self.booking_repository.create_booking(
            room_number=booking_in.room_number,
            guest_name=booking_in.guest_name,
            check_in=check_in,
            check_out=check_out,
            user_id=current_user.id,
            unique_id=unique_id,
        )
        return BookingResponse.model_validate(booking)