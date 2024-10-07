import uuid
from flask import request, jsonify
from flask_login import login_user
from flasgger import swag_from

from trade import app, db
from trade.dao import auth
from trade.model import UserProfile
from trade.utils import token

@app.route('/api/login', methods=['POST'])
@swag_from({
    'summary': 'Login a user',
    'description': 'This endpoint logs in a user using username/password or Google ID.',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'schema': {
                'type': 'object',
                'properties': {
                    'username': {'type': 'string'},
                    'password': {'type': 'string'},
                    'google_id': {'type': 'string'}
                },
                'required': ['username', 'password']
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'Login successful',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'},
                    'user_id': {'type': 'integer'},
                    'token': {'type': 'string'}
                }
            }
        },
        '401': {
            'description': 'Invalid credentials'
        }
    }
})
def login_user_guest():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    google_id = data.get('google_id')

    print(f"Received data: username={username}, google_id={google_id}")

    user_auth = None
    user = None

    if google_id:
        user_auth = auth.get_user_auth_by_google_id(google_id)
        if user_auth:
            user = user_auth.user
    else:
        user_auth = auth.auth_user(username, password)
        if user_auth:
            user = user_auth

    if user:
        login_user(user)
        new_token = token.create_jwt_token(user)
        return jsonify({'message': 'Login successful', 'user_id': user.idUser, 'token': new_token})

    return jsonify({'message': 'Invalid credentials'}), 401


@app.route('/api/register', methods=['POST'])
@swag_from({
    'summary': 'Register a new user',
    'description': 'This endpoint registers a new user and creates a user profile.',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'schema': {
                'type': 'object',
                'properties': {
                    'username': {'type': 'string'},
                    'first_name': {'type': 'string'},
                    'last_name': {'type': 'string'},
                    'email': {'type': 'string'},
                    'password': {'type': 'string'},
                    'google_id': {'type': 'string'},
                    'phone_number': {'type': 'string'},
                    'need': {'type': 'string'}
                },
                'required': ['username', 'first_name', 'last_name', 'email', 'password']
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'User registered successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'},
                    'user_id': {'type': 'integer'}
                }
            }
        },
        '400': {
            'description': 'Username or email already exists'
        }
    }
})
def register():
    data = request.json
    username = data.get('username')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    password = data.get('password')
    google_id = data.get('google_id')
    phone_number = data.get('phone_number')
    need = data.get('need')

    if auth.get_user_by_username(username):
        return jsonify({'message': 'Username already exists'}), 400

    if auth.get_user_by_email(email):
        return jsonify({'message': 'Email already registered'}), 400

    user = auth.create_user(username, password, email)
    user_profile = UserProfile(idProfile=str(uuid.uuid4()), idUser=user.idUser, phoneNumber=phone_number, need=need, firstName=first_name, lastName=last_name)
    db.session.add(user_profile)
    db.session.commit()

    auth.create_user_auth(user.idUser, google_id=google_id)

    return jsonify({'message': 'User registered successfully', 'user_id': user.idUser})


@app.route('/api/current-user', methods=['GET'])
@swag_from({
    'summary': 'Get the current user information',
    'description': 'This endpoint retrieves the information of the currently authenticated user.',
    'responses': {
        '200': {
            'description': 'Current user details',
            'schema': {
                'type': 'object',
                'properties': {
                    'user_id': {'type': 'integer'},
                    'username': {'type': 'string'},
                    'email': {'type': 'string'},
                    'first_name': {'type': 'string'},
                    'last_name': {'type': 'string'},
                    'phone_number': {'type': 'string'},
                    'registration_complete': {'type': 'boolean'}
                }
            }
        },
        '401': {
            'description': 'Invalid token or missing authorization'
        },
        '404': {
            'description': 'User not found'
        }
    }
})
def get_current_user():
    auth_header = request.headers.get('Authorization')

    if auth_header and auth_header.startswith('Bearer '):
        jwt_token = auth_header.split(' ')[1]

        try:
            decoded_token = token.decode_token(jwt_token)
            user_id = decoded_token.get('user_id')

            user = auth.get_user_by_id(user_id)
            user_profile = UserProfile.query.filter_by(idUser=user_id).first()

            if not user:
                return jsonify({'message': 'User not found'}), 404

            user_info = {
                'user_id': user.idUser,
                'email': user.email,
                'first_name': user_profile.firstName,
                'last_name': user_profile.lastName,
                'phone_number': user_profile.phoneNumber,
                'need': user_profile.need
            }
            return jsonify({'user': user_info}), 200

        except Exception as e:
            return jsonify({'message': 'Invalid token', 'error': str(e)}), 401

    else:
        return jsonify({'message': 'Authorization header is missing or invalid'}), 401
