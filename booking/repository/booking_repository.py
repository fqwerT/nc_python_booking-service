from datetime import datetime

from sqlalchemy import and_, or_
from sqlalchemy.orm import Session
from rooms.model.rooms_model import Room
from booking.model.booking_model import Booking


class BookingRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_all_bookings(self) -> list[Booking]:
        return self.db_session.query(Booking).all()
    
    def deleteBooking(self,id) -> bool:
        booking_to_delete = self.db_session.query(Booking).filter(Booking.id == id).one()
        if booking_to_delete:
           self.db_session.delete(booking_to_delete)
           self.db_session.commit()
           return True
        else:
           return False
        
    def update_booking(self, booking_update: Booking) -> Booking:
        booking_to_update = self.db_session.query(Booking).filter(Booking.id == booking_update.id).first()
        if not booking_to_update:
            raise ValueError(f"Booking with id {booking_update.id} not found")
    
        for key, value in booking_update.dict(exclude_unset=True).items():
            setattr(booking_to_update, key, value)
            self.db_session.commit()
            self.db_session.refresh(booking_to_update)
    
            return booking_to_update
        
    def get_bookings_by_room_ID(self, id) -> list[Booking]:
        return self.db_session.query(Booking).filter(Booking.room_id == id).all()
    
    def get_bookings_by_user_ID(self, id) -> list[Booking]:
        return self.db_session.query(Booking).filter(Booking.user_id == id).all()

    def create_booking(
    self,
    *,
    room_id: str,
    guest_name: str,
    check_in: datetime,
    check_out: datetime,
    user_id: str,
    status: str = "confirmed",
    unique_id: str
) -> Booking:
        booking = Booking(
        room_id=room_id,
        guest_name=guest_name,
        check_in=check_in,
        check_out=check_out,
        user_id=user_id,
        status=status,
        id=unique_id,
        
    )
        self.db_session.add(booking)
        self.db_session.commit()
        self.db_session.refresh(booking)
        return booking

    def get_overlapping_bookings(self, *, room_id: str, start: datetime, end: datetime) -> list[Booking]:
        query = self.db_session.query(Booking).filter(
            Booking.room_id == room_id,
            Booking.check_in < end,
            Booking.check_out > start,
        )

    
        return query.all()