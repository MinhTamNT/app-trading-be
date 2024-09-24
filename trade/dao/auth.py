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

def create_user(username, password , email):
    user = User(idUser=str(uuid.uuid4()), username=username, email=email , password =  hashlib.sha256(password.encode('utf-8')).hexdigest())
    db.session.add(user)
    db.session.commit()
    return user

def create_user_auth(user_id, google_id=None):
    user_auth = UserAuth(idAuth=str(uuid.uuid4()), userId=user_id, googleId=google_id)
    db.session.add(user_auth)
    db.session.commit()
    return user_auth

def auth_user(username, password):
    password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    print(f"Authenticating user: {username}, Password hash: {password_hash}")
    return User.query.filter_by(username=username.strip(), password=password_hash).first()

def get_user(user_id):
    user = get_user_by_id(user_id)
    if user:
        print(f"User found: {user.username}")
    else:
        print("User not found.")
    return user


def delete_user(user_id):
    user = get_user_by_id(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        print(f"User {user.username} deleted successfully.")
    else:
        print("User not found.")


def get_all_users():
    users = User.query.all()
    if users:
        print(f"Found {len(users)} users.")
    else:
        print("No users found.")
    return users


