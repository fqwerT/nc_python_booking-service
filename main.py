import logging
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from booking.controller.booking_controller import router as booking_router
from auth.controller.auth_controller import router as auth_router

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Room Booking Service",
    description="Сервис бронирования переговорных комнат с JWT‑авторизацией.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)



app.include_router(booking_router, prefix="/bookings", tags=["bookings"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])
