from flask import Flask, render_template

from trade import app
from trade.api.auth import auth


@app.route("/")
def index():
    return render_template("home.html")


if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)
