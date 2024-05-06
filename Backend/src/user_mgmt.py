from init_db import *
from utils import create_session
import hashlib


class User_MGMT:
    def __init__(self, engine):
        self.engine = engine

    def user_lookup(self, email):
        session = create_session(self.engine)
        result = (
            session.query(User.username, User.user_id)
            .filter(User.email == email)
            .one_or_none()
        )
        if result == None:
            return False, None, None
        session.close()
        return True, result[0], result[1]

    def user_lookup(self, user_id):
        session = create_session(self.engine)
        result = (
            session.query(User.username, User.user_id, User.email, User.created_on)
            .filter(User.user_id == user_id)
            .one_or_none()
        )
        if result == None:
            return False, None, None, None, None
        # Check if the result contains the car id
        car_id = "User Has Not Picked a Car"
        if hasattr(result, 'car_id'):
            car_id = result.car_id

        session.close()
        return True, result[0], result[1], result[2], result[3], car_id

    def user_exists(self, username):
        session = create_session(self.engine)
        result = session.query(User.user_id).where(User.username == username).scalar()
        session.close()
        return result != None

    def create_user(self, username, email_address, password):
        session = create_session(self.engine)
        password_hash = hashlib.sha256(password.encode()).digest()
        new_user = User(
            username=username, email=email_address, password_hash=password_hash
        )
        session.add(new_user)
        session.commit()
        session.close()
