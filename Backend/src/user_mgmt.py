from init_db import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func, cast
from sqlalchemy.sql import exists
from utils import create_session
import hashlib

def user_lookup(email):
    
    session = create_session()
    
    result = (session.query(User.username, User.user_id)
              .filter(User.email == email)
              .one_or_none())
    
    if result == None:
        return False, None, None
    
    session.close()
    return True, result[0], result[1]


def user_exists(username):

    session = create_session()

    result = (session.query(User.user_id)
                            .where(User.username == username)
                            .scalar())

    session.close()
    return result != None


def create_user(username, email_address, password):
    session = create_session()

    password_hash = hashlib.sha256(password.encode()).digest()
    new_user = User(username = username,
                    email = email_address,
                    password_hash = password_hash)
    
    session.add(new_user)

    session.commit()

    session.close()

