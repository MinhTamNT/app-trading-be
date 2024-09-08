import enum
import hashlib

from sqlalchemy import Column, String, Enum, DateTime, ForeignKey, Text, Integer, Boolean
from sqlalchemy.orm import relationship
from trade.trade import  db, app
from flask_login import UserMixin
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

class User(db.Model , UserMixin):
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

    @property
    def is_active(self):
        """Flask-Login requires this property to determine if the user is active."""
        return self.isActive

    def get_id(self):
        return self.idUser

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
    phoneNumber = Column(String(20), unique=True, nullable=True)
    provider = Column(Enum('starand', 'google'), nullable=False)

    user = relationship('User', back_populates='auth')

class UserProfile(db.Model):
    __table_args__ = {'extend_existing': True}
    idProfile = Column(String(255), primary_key=True)
    firstName = Column(String(150), nullable=True)
    lastName = Column(String(150), nullable=True)
    profileImage = Column(String(250), nullable=True)
    phoneNumber = Column(Integer, nullable=True)
    need = Column(Enum('AUTO_TRADE', 'NOTIFICATION'), nullable=True)
    idUser = Column(String(255), ForeignKey('user.idUser'), nullable=False)

    user = relationship('User', back_populates='profile')

if __name__ == '__main__':
    with app.app_context():
        # db.create_all()
        # password = hashlib.md5("123".encode("utf-8")).hexdigest()
        #
        # # Create an admin user
        # admin_user = User(
        #     idUser="e1175186-ead1-418d-92fc-9ba7edaf700b",  # Unique user ID
        #     username="admin",  # Admin username
        #     email="admin@example.com",  # Admin email
        #     password=password,  # Hashed password
        #     isActive=True,  # Active status
        #     userRole=UserRole.ADMIN  # Assign ADMIN role
        # )
        #
        # db.session.add(admin_user)
        #
        # db.session.commit()
        #
        # print(f"Admin user '{admin_user.username}' with role '{admin_user.userRole.name}' created.")
        print("Database tables created.")