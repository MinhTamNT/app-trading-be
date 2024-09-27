import uuid
from datetime import datetime

from trade import db
from trade.model import Recommendation, User


def create_recommend_stock(symbol, type_, date_str , price, username , current_price):
    try:
        idRecommend = str(uuid.uuid4())

        user = User.query.filter_by(username=username).first()
        if not user:
            return {'status': 'error', 'message': 'User not found'}, 404

        new_recommendation = Recommendation(
            idRecommend=idRecommend,
            symbol=symbol,
            type=type_,
            date=date_str,
            price = price ,
            priceRecommend = current_price
        )

        db.session.add(new_recommendation)
        db.session.commit()
        print("da add")

        return {'status': 'success', 'message': 'Stock recommendation created successfully', 'idRecommend': idRecommend}

    except Exception as e:
        db.session.rollback()
        return {'status': 'error', 'message': str(e)}
