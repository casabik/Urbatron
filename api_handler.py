from fastapi import APIRouter, Body, Depends, Header
from models import User, Place, Parking, Booking, connection
from forms import UserRegistration, UserLoginForm, PlaceForm, ParkingForm, BookingForm
import jwt
import uuid
from peewee import *

router = APIRouter()


SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"


@router.post("/login")
async def login(user_data: UserLoginForm):
    user = User.get(user_data.login)
    if not user or user_data.password != user["password"]:
        return {"message": "Invalid login or password"}
    token_content = {"user_id": user["user_id"]}
    jwt_token = jwt.encode(token_content, SECRET_KEY, algorithm=ALGORITHM)
    return {"token": jwt_token}



@router.post("/registration")
async def registration(user_data: UserRegistration):
    try:
        new_user = User.create(login=user_data.login, password=user_data.password)
        new_user.save()
        return {"message": "User registered successfully"}
    except IntegrityError:
        return {"message": "User with this login already exists"}


@router.post("/create_place")
async def create_place(place_data: PlaceForm, authorization: str = Header(None)):
    payload = jwt.decode(authorization, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload.get("user_id")
    if user_id is None:
        return {"message": "Invalid token"}
    new_place = Place.create(
        user_id=user_id,
        name=place_data.name,
        latitude=place_data.latitude,
        longitude=place_data.longitude
    )
    new_place.save()
    place_id = new_place.place_id
    user = User.get(User.user_id == user_id)
    if user.user_places == "":
        user.user_places = str(place_id)
    else:
        user.user_places = user.user_places + "," + str(place_id) 
    user.save()
    return {"message": "Place created successfully"}

@router.post("/create_parking")
async def create_parking(place_data: ParkingForm):
    new_parking = Parking.create(
        number_spaces=place_data.number_spaces,
        latitude=place_data.latitude,
        longitude=place_data.longitude
    )
    new_parking.save()
    return {"message": "Parking created successfully"}

@router.get("/get_places")
async def create_parking(authorization: str = Header(None)):
    payload = jwt.decode(authorization, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload.get("user_id")
    places = User.get(User.user_id == user_id).user_places
    if places == "":
        return {"message": "No places found"}
    else:
        array_places = []
        places = places.split(",")
        for place in places:
            place_info = Place.get(Place.place_id == place)
            temp_dict = {
                "name": place_info.name,
                "latitude": place_info.latitude,
                "longitude": place_info.longitude
            }
            array_places.append(temp_dict)        
        return {"places": array_places}

@router.post("/book_place")
async def book_place(book_data: BookingForm, authorization: str = Header(None)):
    payload = jwt.decode(authorization, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload.get("user_id")
    new_booking = Booking.create(
        parking_id=book_data.parking_id,
        numper_spaces=book_data.numper_spaces,
        user_id=user_id,
        start_date=book_data.start_date,
        end_date=book_data.end_date
    )
    new_booking.save()
    return {"message": "Booking created successfully"}


@router.get("/get_bookings")
async def get_bookings(authorization: str = Header(None)):
    payload = jwt.decode(authorization, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload.get("user_id")
    bookings = Booking.select().where(Booking.user_id == user_id)
    if bookings == "":
        return {"message": "No bookings found"}
    else:
        array_bookings = []
        for booking in bookings:
            parking = Parking.get(Parking.parking_id == booking.parking_id)
            latitude = parking.latitude
            longitude = parking.longitude
            temp_dict = {
                "latitude": latitude,
                "longitude": longitude,
                "numper_spaces": booking.numper_spaces,
                "start_date": booking.start_date,
                "end_date": booking.end_date
            }
            array_bookings.append(temp_dict)
        return {"bookings": array_bookings}