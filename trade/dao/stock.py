import uuid
from datetime import datetime

from trade import db
from trade.model import Recommendation


def create_recommend_stock(symbol, type_, date_str):
    try:
        idRecommend = str(uuid.uuid4())

        try:
            date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            return {'status': 'error', 'message': 'Invalid date format. Expected format: YYYY-MM-DDTHH:MM:SS'}

        # Create a new Recommendation instance
        new_recommendation = Recommendation(
            idRecommend=idRecommend,
            symbol=symbol,
            type=type_,
            date=date
        )

        db.session.add(new_recommendation)
        db.session.commit()

        return {'status': 'success', 'message': 'Stock recommendation created successfully', 'idRecommend': idRecommend}

    except Exception as e:
        db.session.rollback()
        return {'status': 'error', 'message': str(e)}
