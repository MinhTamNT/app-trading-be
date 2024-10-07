from trade import db
from trade.model import Recommendation, SignalSell, SignalBuy


def get_recommendations_all():
    try:
        recommendations = db.session.query(Recommendation).all()
        return recommendations
    except Exception as e:
        print(f"An error occurred while fetching recommendations: {e}")
        return []


def get_all_recommendations_api():

    sold_buy_ids = db.session.query(SignalSell.buy_id).all()
    sold_buy_ids = [sell_id[0] for sell_id in sold_buy_ids]

    recommendations = SignalBuy.query.filter(SignalBuy.id.notin_(sold_buy_ids)).all()

    print(recommendations)

    return [
        {
            'id': rec.id,
            'symbol': rec.stock,
            'date': rec.last_update,
            'priceRecommend': rec.price_recommend,
            'current_price': rec.last_price,
            'profit': rec.profit,
        }
        for rec in recommendations
    ]



