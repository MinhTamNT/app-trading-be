from urllib import request

from flask import render_template, redirect, url_for , request
from flask_login import login_user, login_required, logout_user, current_user

from . import login
from .model import *
from .dao import auth



@login.user_loader
def load_user(user_id):
    user = User.query.get(user_id)
    print(user)
    return user

@app.route("/admin/login", methods=['GET', 'POST'])
def login():
    message = ""
    if request.method.__eq__("POST"):
        username = request.form['username']
        password = request.form['password']
        user = auth.auth_user(username, password)
        print(user)
        if user:
            login_user(user=user)
            return redirect(url_for('index'))
        message = "Invalid username or password"
    return render_template('login.html', message=message)


@app.route('/')
def index():
    print(current_user.is_authenticated)
    if current_user.is_authenticated:
        return render_template('index.html' , current_user=current_user)
    return redirect(url_for('login'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)
        app.run(host='0.0.0.0', port=5000)
