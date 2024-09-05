from flask_login import UserMixin
from sqlalchemy import Column, String, ForeignKey, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from trade import db, app
import uuid

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    idUser = Column(String(255), primary_key=True)
    username = Column(String(150), unique=True, nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=db.func.current_timestamp())
    updated_at = Column(DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Quan hệ với bảng UserAuth và UserProfile
    auth = relationship('UserAuth', uselist=False, back_populates='user', cascade="all, delete-orphan")
    profile = relationship('UserProfile', uselist=False, back_populates='user', cascade="all, delete-orphan")

    def get_id(self):
        return str(self.idUser)

class UserAuth(db.Model):
    __tablename__ = 'user_auth'

    idAuth = Column(String(255), primary_key=True)
    user_id = Column(String(255), ForeignKey('users.idUser'), nullable=False)
    password_hash = Column(String(8000), nullable=True)
    google_id = Column(String(200), nullable=True, unique=True)
    phone_number = Column(String(20), nullable=True, unique=True)
    provider = Column(Enum('starand', 'google', name='auth_providers'), nullable=False , default='starand')

    user = relationship('User', back_populates='auth')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_google_login(self):
        return self.provider == 'google'


class UserProfile(db.Model):
    __tablename__ = 'user_profiles'

    idProfile = Column(String(255), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(255), ForeignKey('users.idUser'), nullable=False)
    first_name = Column(String(150), nullable=True)
    last_name = Column(String(150), nullable=True)
    profile_image = Column(String(250), nullable=True)
    phone_number = Column(String(20), nullable=True)
    registration_complete = Column(String(50), default=False)

    user = relationship('User', back_populates='profile')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
