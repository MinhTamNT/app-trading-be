import uuid
from datetime import datetime

from trade import db
from trade.model import Recommendation, User


def calculate_profit(current_price, purchase_price):
    if purchase_price == 0:
        return 0
    return ((current_price - purchase_price) / purchase_price) * 100

def create_recommend_stock(symbol, type_, date_str, price, username, current_price):
    try:
        idRecommend = str(uuid.uuid4())

        user = User.query.filter_by(username=username).first()
        if not user:
            return {'status': 'error', 'message': 'User not found'}, 404

        profit = calculate_profit(current_price, price)

        new_recommendation = Recommendation(
            idRecommend=idRecommend,
            symbol=symbol,
            type=type_,
            lastUpdate=date_str,
            price=price,
            priceRecommend=current_price,
            profit=profit
        )
        print(new_recommendation)
        db.session.add(new_recommendation)
        db.session.commit()
        print("da add")

        return {'status': 'success', 'message': 'Stock recommendation created successfully', 'idRecommend': idRecommend}

    except Exception as e:
        db.session.rollback()
        return {'status': 'error', 'message': str(e)}

def update_recommend_stock(name_symbol, new_price, date_str, current_price):
    try:
        recommendation = Recommendation.query.filter_by(symbol=name_symbol).first()
        if not recommendation:
            return {'status': 'error', 'message': 'Recommendation not found'}, 404

        # Update fields
        recommendation.price = new_price
        recommendation.lastUpdate = date_str
        recommendation.profit = calculate_profit(current_price, new_price)

        db.session.commit()

        return {'status': 'success', 'message': 'Stock recommendation updated successfully'}

    except Exception as e:
        db.session.rollback()
        return {'status': 'error', 'message': str(e)}


def find_recommendation_by_symbol(symbol):

    return Recommendation.query.filter_by(symbol=symbol).first()