from pydantic import BaseModel

class UserLoginForm(BaseModel):
    login: str
    password: str


class Registration(BaseModel):
    login: str
    password: str

class Place(BaseModel):
    name: str
    latitude: float
    longitude: float

class Parking(BaseModel):
    name: str
    latitude: float
    longitude: float