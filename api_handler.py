from fastapi import APIRouter, Body, Depends
from form import UserLoginForm, Registration, Parking
from database import database, Token, User, Parking, Place
import uuid

router = APIRouter()



@router.post("/login")
async def login(user_from: UserLoginForm = Body(..., embded=True), database=Depends(database)):
    user = database.query(User).filter(User.login == user_from.login).first()
    if not user:
        return {"status": "User not found"}

    token = Token(token=str(uuid.uuid4()), user_id=user.id)
    database.add(token)
    database.commit()
    return {"token": token.token}


@router.post("/registration")
async def registration(reg: Registration = Body(..., embded=True), database=Depends(database)):
    login = reg.login
    password = reg.password

    if not database.query(User).filter(User.login == login).first():
        user = User(login=login, password=password, id=str(uuid.uuid4()))
        database.add(user)
        database.commit()
    
    return 'ok'

@router.post("/create_place")
async def create_place(place:Place = Body(..., embded=True), database=Depends(database)):

    place_name = place.name
    lat = place.latitude
    lon = place.longitude
    some_place = Parking(name=place_name, latitude=lat, longitude=lon, id=str(uuid.uuid4()))
    database.add(some_place)
    database.commit()

    return 'ok'

@router.post("/create_parking")
async def create_place(park: Parking = Body(..., embded=True), database=Depends(database)):

    place_name = park.name
    lat = park.latitude
    lon = park.longitude
    parking_place = Parking(name=place_name, latitude=lat, longitude=lon, id=str(uuid.uuid4()))
    database.add(parking_place)
    database.commit()

    return 'ok'

'''
@router.get("/get_places")
async def create_place(park: Parking = Body(..., embded=True), database=Depends(database)):'''