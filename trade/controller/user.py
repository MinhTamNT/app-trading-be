from flask import flash, redirect, url_for

from trade import app
from trade.dao.auth import delete_user


@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user_route(user_id):
    # Call the delete_user function with the provided user_id
    success, username = delete_user(user_id)

    # Check if the deletion was successful
    if success:
        flash(f"User {username} deleted successfully.", 'success')
    else:
        flash("User not found.", 'error')

    return redirect(url_for('index'))