from flask import request, jsonify
from flask_login import login_user

from trade.trade.model import UserProfile
from trade.trade import db, app
from trade.trade.dao import auth

from trade.trade.utils import token


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    google_id = data.get('google_id')

    user_auth = None

    if google_id:
        user_auth = auth.get_user_auth_by_google_id(google_id)
        if user_auth:
            user = user_auth.user
            login_user(user)
            new_token = token.create_jwt_token(user)
            return jsonify({'message': 'Google login successful', 'user_id': user.idUser, 'token': new_token})
    else:
        user_auth = auth.get_user_auth_by_username(username)
        if user_auth and user_auth.check_password(password):
            user = user_auth.user
            login_user(user)
            new_token = token.create_jwt_token(user)
            return jsonify({'message': 'Login successful', 'user_id': user.idUser, 'token': new_token})

    return jsonify({'message': 'Invalid credentials'}), 401



@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    password = data.get('password')
    google_id = data.get('google_id')
    phone_number = data.get('phone_number')
    registration_complete = data.get('registration_complete')

    if auth.get_user_by_username(username):
        return jsonify({'message': 'Username already exists'}), 400

    if auth.get_user_by_email(email):
        return jsonify({'message': 'Email already registered'}), 400

    user = auth.create_user(username, email)
    user_profile = UserProfile(user_id=user.idUser, phone_number=phone_number, registration_complete=registration_complete , first_name=first_name, last_name=last_name)
    db.session.add(user_profile)
    db.session.commit()

    auth.create_user_auth(user.idUser, google_id=google_id, password=password)

    return jsonify({'message': 'User registered successfully', 'user_id': user.idUser})


@app.route('/current-user', methods=['GET'])
def get_current_user():
    auth_header = request.headers.get('Authorization')

    if auth_header and auth_header.startswith('Bearer '):
        jwt_token = auth_header.split(' ')[1]  # Get the actual token part

        try:
            # Decode the JWT token
            decoded_token = token.decode_token(jwt_token)

            # Get the user_id from the decoded token
            user_id = decoded_token.get('user_id')

            # Query the user info based on user_id
            user = auth.get_user_by_id(user_id)
            user_profile = UserProfile.query.filter_by(user_id=user_id).first()

            if not user:
                return jsonify({'message': 'User not found'}), 404

            # Return the user's information
            user_info = {
                'user_id': user.idUser,
                'username': user.username,
                'email': user.email,
                'first_name': user_profile.first_name,
                'last_name': user_profile.last_name,
                'phone_number': user_profile.phone_number,
                'registration_complete': user_profile.registration_complete
            }
            return jsonify({'user': user_info}), 200

        except Exception as e:
            return jsonify({'message': 'Invalid token', 'error': str(e)}), 401

    else:
        return jsonify({'message': 'Authorization header is missing or invalid'}), 401

# if __name__ == '__main__':
#     with app.app_context():
#         app.run(debug=True)
