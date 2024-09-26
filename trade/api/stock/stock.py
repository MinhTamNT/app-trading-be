from flask import request, jsonify
from flask_login import login_required
from flasgger import swag_from

from trade import app
from trade.dao.stock import create_recommend_stock
from trade.utils.authorize import authen_required


@app.route('/api/stock/create-stock', methods=['POST'])
@authen_required
@swag_from({
    'summary': 'Create a stock recommendation',
    'description': 'This endpoint allows users to create a stock recommendation by providing stock details such as symbol, type, and date.',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'schema': {
                'type': 'object',
                'properties': {
                    'symbol': {
                        'type': 'string',
                        'description': 'The stock symbol, e.g., AAPL, GOOG',
                        'example': 'AAPL'
                    },
                    'type': {
                        'type': 'string',
                        'description': 'The type of stock, e.g., buy, sell',
                        'example': 'buy'
                    },
                    '    ': {
                        'type': 'string',
                        'description': 'The date for the stock recommendation in YYYY-MM-DD format',
                        'example': '2024-09-20'
                    }
                },
                'required': ['symbol', 'type', 'date']
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'Stock recommendation created successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string', 'example': 'success'},
                    'message': {'type': 'string'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'symbol': {'type': 'string'},
                            'type': {'type': 'string'},
                            'date': {'type': 'string'}
                        }
                    }
                }
            }
        },
        '400': {
            'description': 'Missing required parameters',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string', 'example': 'error'},
                    'message': {'type': 'string', 'example': 'Missing required parameters'}
                }
            }
        }
    }
})
def create_stock():
    data = request.get_json()

    # Extract the parameters
    symbol = data.get('symbol')
    type_ = data.get('type')
    date_str = data.get('date')
    price = data.get('price')
    if not symbol or not type_ or not date_str:
        return jsonify({'status': 'error', 'message': 'Missing required parameters'}), 400

    result = create_recommend_stock(symbol, type_, date_str , price)
    print(result)
    return jsonify(result)
