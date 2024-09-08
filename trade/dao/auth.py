import hashlib

from ..model import *
import uuid

def get_user_by_id(user_id):
    return User.query.get(user_id)

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_user_by_email(email):
    return User.query.filter_by(email=email).first()

def get_user_auth_by_google_id(google_id):
    return UserAuth.query.filter_by(google_id=google_id).first()

def get_user_auth_by_username(username):
    return UserAuth.query.join(User).filter(User.username == username).first()

def create_user(username, email):
    user = User(idUser=str(uuid.uuid4()), username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return user

def create_user_auth(user_id, google_id=None, password=None):
    user_auth = UserAuth(idAuth=str(uuid.uuid4()), user_id=user_id, google_id=google_id)
    if password:
        user_auth.set_password(password)
    db.session.add(user_auth)
    db.session.commit()
    return user_auth

def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    print(password)
    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()
