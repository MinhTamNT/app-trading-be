
from flask import request, jsonify
from flasgger import swag_from
from flask_wtf.file import file_allowed

from trade import app
from trade.dao.stock import create_recommend_stock, update_recommend_stock, find_recommendation_by_symbol
from trade.dao.recommend import *

from flask_socketio import emit

from trade.model import SignalSell, SignalBuy


@app.route('/api/stock/create-or-update-stock', methods=['POST'])
@swag_from({
    'summary': 'Create or update a stock recommendation',
    'description': 'This endpoint allows users to create a new stock recommendation or update an existing one by providing stock details such as symbol, type, date, price, and current price.',
    'parameters': [
        # Swagger documentation details
    ],
    'responses': {
        # Response details
    }
})
def create_or_update_stock():
    data = request.get_json()
    username = request.args.get('username')

    symbol = data.get('symbol')
    type_ = data.get('type')
    date_str = data.get('date')
    price = data.get('price')
    current_price = data.get('current_price')
    interval = data.get('interval')
    resolution = data.get('resolution')
    if not symbol or not type_ or not date_str or not price or not current_price or not username:
        return jsonify({'status': 'error', 'message': 'Missing required parameters'}), 400

    type_ = int(type_)
    existing_recommendations = SignalBuy.query.filter_by(stock=symbol).all()
    print(existing_recommendations)

    if existing_recommendations:
        buy_ids = [recommendation.id for recommendation in existing_recommendations]

        sell_signals = SignalSell.query.filter(SignalSell.buy_id.in_(buy_ids)).all()
        print(sell_signals)

        sold_buy_ids = [sell_signal.buy_id for sell_signal in sell_signals]
        print(sold_buy_ids)

        if not sold_buy_ids:
            print("No sell signals found, updating all buy signals.")
            for recommendation in existing_recommendations:
                print(f"Updating price for buy signal {recommendation.id} as no sell signal exists...")
                update_recommend_stock(recommendation.id, current_price, date_str)
        else:
            for recommendation in existing_recommendations:
                if recommendation.id in sold_buy_ids:
                    print(f"Buy signal {recommendation.id} has an associated sell signal, skipping update.")
                else:

                    if type_ == 1:
                        print(f"Updating price for buy signal {recommendation.id} as no sell signal exists...")
                        update_recommend_stock(recommendation.id, current_price, date_str)

                    else:
                        print(f"Creating a new recommendation for stock {symbol}.")
                        create_recommend_stock(symbol, type_, date_str, price, username, current_price, interval,
                                               resolution)

    else:
        print(f"No existing buy recommendations found, creating a new one for stock {symbol}.")
        create_recommend_stock(symbol, type_, date_str, price, username, current_price, interval, resolution)


    return jsonify({
        'status': 'success',
        'message': 'Stock recommendation created or updated successfully'
    }), 200


@app.route('/api/stock/recommendations', methods=['GET'])
@swag_from({
    'summary': 'Get all stock recommendations',
    'description': 'This endpoint retrieves all stock recommendations available in the database.',
    'responses': {
        '200': {
            'description': 'List of stock recommendations retrieved successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string', 'example': 'success'},
                    'data': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'symbol': {'type': 'string'},
                                'type': {'type': 'string'},
                                'date': {'type': 'string'},
                                'price': {'type': 'integer'},
                                'current_price': {'type': 'integer'},
                                'username': {'type': 'string'}
                            }
                        }
                    }
                }
            }
        },
        '404': {
            'description': 'No recommendations found',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string', 'example': 'error'},
                    'message': {'type': 'string', 'example': 'No recommendations found'}
                }
            }
        }
    }
})
def get_stock_recommendations():
    recommendations = get_all_recommendations_api()

    # if recommendations:
    #     emit('recommendations_fetched', recommendations)
    #     print("connect")
    if not recommendations:
        return jsonify({
            'message': 'No recommendations found'
        }), 200

    return jsonify({
        'status': 'success',
        'data': recommendations
    }), 200