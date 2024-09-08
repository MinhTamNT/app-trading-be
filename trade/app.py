from urllib import request

from flask import render_template, redirect, url_for , request
from flask_login import login_user, login_required, logout_user, current_user

from trade.trade import login
from trade.trade.model import *
from trade.trade.dao import auth


@login.user_loader
def load_user(user_id):
    return  User.query.get(user_id)


@app.route("/login", methods=['GET', 'POST'])
def login_admin():
    message = "Invalid username or password"
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = auth.auth_user(username, password)
        if user:
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html', message=message)


@app.route('/')
def index():
    if current_user.is_authenticated:
        return "<p>Welcome to Trade</p>"
    return redirect(url_for('login_admin'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return "<p>You have been logged out.</p>"

if __name__ == '__main__':
    with app.app_context():
        app.run(host='0.0.0.0', port=5000)
