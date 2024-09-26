import uuid
from datetime import datetime

from trade import db
from trade.model import Recommendation


def create_recommend_stock(symbol, type_, date_str , price):
    try:
        idRecommend = str(uuid.uuid4())

        new_recommendation = Recommendation(
            idRecommend=idRecommend,
            symbol=symbol,
            type=type_,
            date=date_str,
            price = price
        )

        db.session.add(new_recommendation)
        db.session.commit()
        print("da add")

        return {'status': 'success', 'message': 'Stock recommendation created successfully', 'idRecommend': idRecommend}

    except Exception as e:
        db.session.rollback()
        return {'status': 'error', 'message': str(e)}
