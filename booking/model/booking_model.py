from sqlalchemy import Column, DateTime, Integer, String, Sequence
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Booking(Base):
    __tablename__ = "bookings"

    # Уникальный идентификатор брони
    id = Column(String(228), primary_key=True, nullable=False, index=True)

    # Номер переговорной комнаты
    room_number = Column(Integer, nullable=False, index=True)

    # Имя гостя / бронирующего (для отображения)
    guest_name = Column(String, nullable=False)

    # Время начала и окончания бронирования
    check_in = Column(DateTime, nullable=False, index=True)
    check_out = Column(DateTime, nullable=False, index=True)

    # Идентификатор пользователя, создавшего бронь
    user_id = Column(String(228), nullable=False, index=True)

    # Статус брони (например: 'confirmed', 'cancelled')
    status = Column(String, nullable=False, default="confirmed")