import enum
import hashlib

from sqlalchemy import Column, String, Enum, DateTime, ForeignKey, Text, Integer, Boolean
from sqlalchemy.orm import relationship

from flask_login import UserMixin

from trade import db, app


class UserRole(enum.Enum):
    ADMIN = 1
    GUEST = 2


class Recommendation(db.Model):
    __table_args__ = {'extend_existing': True}
    idRecommend = Column(String(255), primary_key=True)
    symbol = Column(String(100), nullable=True)
    type = Column(Enum('Buy', 'Sell', 'Hold'), nullable=True)
    date = Column(DateTime, nullable=True)

    notifications = relationship('Notification', back_populates='recommendation')


class User(db.Model, UserMixin):
    __table_args__ = {'extend_existing': True}
    idUser = Column(String(255), primary_key=True)
    username = Column(String(150), unique=True, nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password = Column(String(255), nullable=True)
    isActive = Column(Boolean, default=None)
    createdAt = Column(DateTime, default=db.func.current_timestamp())
    updatedAt = Column(DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    userRole = Column(Enum(UserRole), default=UserRole.GUEST)
    auth = relationship('UserAuth', uselist=False, back_populates='user', cascade="all, delete-orphan")
    profile = relationship('UserProfile', uselist=False, back_populates='user', cascade="all, delete-orphan")
    notifications = relationship('Notification', back_populates='user')
    credentials = relationship('Credentials', back_populates='user')

    # Add the get_id method required by Flask-Login
    def get_id(self):
        return self.idUser

    # Optional: Flask-Login expects this property
    @property
    def is_active(self):
        return self.isActive


class Notification(db.Model):
    __table_args__ = {'extend_existing': True}
    idNotification = Column(String(255), primary_key=True)
    message = Column(String(500), nullable=True)
    typeNotifications = Column(Enum('APP', 'ZALO'), nullable=True)
    idRecommend = Column(String(255), ForeignKey('recommendation.idRecommend'), nullable=False)
    userId = Column(String(255), ForeignKey('user.idUser'), nullable=False)
    createdAt = Column(DateTime, default=db.func.current_timestamp())

    recommendation = relationship('Recommendation', back_populates='notifications')
    user = relationship('User', back_populates='notifications')


class Credentials(db.Model):
    __table_args__ = {'extend_existing': True}
    idCredentials = Column(String(255), primary_key=True)
    CustomerID = Column(String(255), unique=True, nullable=True)
    CustomerSecret = Column(String(255), nullable=True)
    PrivateKey = Column(Text, nullable=True)
    idUser = Column(String(255), ForeignKey('user.idUser'), nullable=False)

    user = relationship('User', back_populates='credentials')


class UserAuth(db.Model):
    __table_args__ = {'extend_existing': True}
    idAuth = Column(String(255), primary_key=True)
    userId = Column(String(255), ForeignKey('user.idUser'), nullable=False)
    googleId = Column(String(200), unique=True, nullable=True)
    provider = Column(Enum('strand', 'google'), nullable=False ,default="strand")

    user = relationship('User', back_populates='auth')


class UserProfile(db.Model):
    __table_args__ = {'extend_existing': True}
    idProfile = Column(String(255), primary_key=True)
    firstName = Column(String(150), nullable=True)
    lastName = Column(String(150), nullable=True)
    profileImage = Column(String(250), nullable=True)
    phoneNumber = Column(String(20), nullable=True)
    need = Column(Enum('AUTO_TRADE', 'NOTIFICATION'), nullable=True)
    idUser = Column(String(255), ForeignKey('user.idUser'), nullable=False)

    user = relationship('User', back_populates='profile')

#
# if __name__ == '__main__':
#     with app.app_context():
#         # db.create_all()
#         for i in range(1, 11):  # Create 10 users
#             # Generate a random username and email
#             username = f"user{i}"
#             email = f"user{i}@example.com"
#             password = hashlib.sha256("password123".encode("utf-8")).hexdigest()  # Example password
#
#             # Determine user role (5 admins and 5 guests)
#             user_role = UserRole.ADMIN if i <= 5 else UserRole.GUEST
#
#             # Create user instance
#             user = User(
#                 idUser=str(i),  # Unique user ID
#                 username=username,
#                 email=email,
#                 password=password,
#                 isActive=True,
#                 userRole=user_role
#             )
#
#             # Add user to the session
#             db.session.add(user)
#
#         db.session.commit()
#
#         print("10 users created successfully.")
#         print("Database tables created.")