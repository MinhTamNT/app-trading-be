from flask import flash, redirect, url_for

from trade import app
from trade.dao.auth import delete_user


@app.route('/delete_user/<string:user_id>', methods=['DELETE'])
def delete_user_route(user_id):
    success = delete_user(user_id)
    if success:
        flash(f"User deleted successfully.", 'success')
    else:
        flash("User not found.", 'error')

    return redirect(url_for('manager_account'))