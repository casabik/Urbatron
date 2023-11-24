database = None

class User (database):
    __tablename__ = 'users'
    id = None
    login = None
    password = None


class Token(database):
    __tablename__ = 'auth_token'
    id = None
    token = None

class Parking(database):
    __tablename__ = 'parking'
    id = None
    name = None
    latitude = None
    longitude = None

class Place(database):
    __tablename__ = 'place'
    id = None
    name = None
    latitude = None
    longitude = None