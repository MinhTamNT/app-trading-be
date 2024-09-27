from sqlalchemy import extract, func
from trade import db
from trade.model import User


def get_user_registrations_by_month():
    registrations_by_month = db.session.query(
        extract('year', User.createdAt).label('year'),
        extract('month', User.createdAt).label('month'),
        func.count(User.idUser).label('total_users')
    ).group_by('year', 'month').all()

    # Convert the results to a list of dictionaries
    formatted_results = [
        {'year': row.year, 'month': row.month, 'total_users': row.total_users}
        for row in registrations_by_month
    ]

    print(formatted_results)
    return formatted_results


def get_user_registrations_by_week():
    registrations_by_week = db.session.query(
        extract('year', User.createdAt).label('year'),
        extract('week', User.createdAt).label('week'),
        func.count(User.idUser).label('total_users')
    ).group_by('year', 'week').all()

    # Convert the results to a list of dictionaries
    formatted_results = [
        {'year': row.year, 'week': row.week, 'total_users': row.total_users}
        for row in registrations_by_week
    ]

    print(formatted_results)
    return formatted_results


def get_user_registrations_by_year():
    registrations_by_year = db.session.query(
        extract('year', User.createdAt).label('year'),
        func.count(User.idUser).label('total_users')
    ).group_by('year').all()

    # Convert the results to a list of dictionaries
    formatted_results = [
        {'year': row.year, 'total_users': row.total_users}
        for row in registrations_by_year
    ]

    print(formatted_results)
    return formatted_results
