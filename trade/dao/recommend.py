from trade import db
from trade.model import Recommendation

def get_recommendations_all():
    try:
        recommendations = db.session.query(Recommendation).all()
        return recommendations
    except Exception as e:
        print(f"An error occurred while fetching recommendations: {e}")
        return []


def get_all_recommendations_api():
    recommendations = Recommendation.query.all()
    print(recommendations)
    return [
        {
            'symbol': rec.symbol,
            'type': rec.type,
            'date': rec.lastUpdate,  # Format date as string
            'priceRecommend': rec.priceRecommend,
            'current_price': rec.price,
            "profit" : rec.profit,
        }
        for rec in recommendations
    ]


