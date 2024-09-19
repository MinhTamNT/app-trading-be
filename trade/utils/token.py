import datetime
import jwt

from trade import app

def create_jwt_token(user):
    payload = {
        'user_id': user.idUser,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),  # Token expiration time
        'iat': datetime.datetime.utcnow()  # Issued at
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return token

def decode_token(token):
    try:
        return jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return {'message': 'Token has expired'}
    except jwt.InvalidTokenError:
        return {'message': 'Invalid token'}
