from datetime import datetime

from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from booking.model.booking_model import Booking


class BookingRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_all_bookings(self) -> list[Booking]:
        return self.db_session.query(Booking).all()

    def create_booking(
        self,
        *,
        room_number: int,
        guest_name: str,
        check_in: datetime,
        check_out: datetime,
        user_id: str,
        status: str = "confirmed",
        unique_id:str
    ) -> Booking:
        booking = Booking(
            room_number=room_number,
            guest_name=guest_name,
            check_in=check_in,
            check_out=check_out,
            user_id=user_id,
            status=status,
            id=unique_id
        )
        self.db_session.add(booking)
        self.db_session.commit()
        self.db_session.refresh(booking)
        return booking

    def get_overlapping_bookings(self, *, room_number: int, start: datetime, end: datetime) -> list[Booking]:
        query = self.db_session.query(Booking).filter(
            Booking.room_number == room_number,
            Booking.check_in < end,
            Booking.check_out > start,
        )

    
        return query.all()