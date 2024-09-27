from urllib import request
from flask import render_template, redirect, url_for, request
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.testing.suite.test_reflection import users

from trade import login, app
from trade.dao import auth
from trade.model import User
import trade.api.stock.stock
import trade.api.auth.auth
import trade.controller.user

from trade.dao import statistical

@login.user_loader
def load_user(user_id):
    return  User.query.get(user_id)

@app.route("/admin/login", methods=['GET', 'POST'])
def admin_login():
    message = ""
    if request.method.__eq__("POST"):
        username = request.form['username']
        password = request.form['password']
        user = auth.auth_user(username, password)
        print(user)
        if user:
            login_user(user=user)
            return redirect(url_for('home'))
        message = "Invalid username or password"
    return render_template('login.html', message=message)


@app.route('/admin/manager-users')
def manager_account():
    if current_user.is_authenticated:
        users = auth.get_all_users()
        return render_template('manager_user.html' , current_user=current_user,users = users)
    return redirect(url_for('admin_login'))

@app.route("/")
def home():
    # users = auth.get_all_users()
    monthly_registrations = statistical.get_user_registrations_by_month()
    weekly_registrations = statistical.get_user_registrations_by_week()
    yearly_registrations = statistical.get_user_registrations_by_year()

    # Prepare data for the template
    return render_template(
        'home.html',
        monthly_registrations=monthly_registrations,
        weekly_registrations=weekly_registrations,
        yearly_registrations=yearly_registrations
    )

@app.route("/admin/follow-recommended")
def follow_recommended():
    return render_template("recommended.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("admin_login"))



if __name__ == '__main__':
    with app.app_context():
        app.run(host='0.0.0.0', port=5000 , debug=True)
