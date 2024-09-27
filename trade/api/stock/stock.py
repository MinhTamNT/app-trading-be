

# @app.route('/api/stock/create-stock', methods=['POST'])
# @swag_from({
#     'summary': 'Create a stock recommendation',
#     'description': 'This endpoint allows users to create a stock recommendation by providing stock details such as symbol, type, date, and username as a query parameter.',
#     'parameters': [
#         {
#             'name': 'body',
#             'in': 'body',
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'symbol': {
#                         'type': 'string',
#                         'description': 'The stock symbol, e.g., AAPL, GOOG',
#                         'example': 'AAPL'
#                     },
#                     'type': {
#                         'type': 'string',
#                         'description': 'The type of stock, e.g., buy, sell',
#                         'example': 'buy'
#                     },
#                     'date': {
#                         'type': 'string',
#                         'description': 'The date for the stock recommendation in YYYY-MM-DD format',
#                         'example': '2024-09-20'
#                     }
#                 },
#                 'required': ['symbol', 'type', 'date']
#             }
#         },
#         {
#             'name': 'username',
#             'in': 'query',
#             'type': 'string',
#             'description': 'The username of the user making the recommendation',
#             'required': True,
#             'example': 'john_doe'
#         }
#     ],
#     'responses': {
#         '200': {
#             'description': 'Stock recommendation created successfully',
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'status': {'type': 'string', 'example': 'success'},
#                     'message': {'type': 'string'},
#                     'data': {
#                         'type': 'object',
#                         'properties': {
#                             'symbol': {'type': 'string'},
#                             'type': {'type': 'string'},
#                             'date': {'type': 'string'},
#                             'username': {'type': 'string'}
#                         }
#                     }
#                 }
#             }
#         },
#         '400': {
#             'description': 'Missing required parameters',
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'status': {'type': 'string', 'example': 'error'},
#                     'message': {'type': 'string', 'example': 'Missing required parameters'}
#                 }
#             }
#         }
#     }
# })
# def create_stock():
#     data = request.get_json()
#
#     username = request.args.get('username')
#
#     symbol = data.get('symbol')
#     type_ = data.get('type')
#     date_str = data.get('date')
#     price = data.get('price')
#     current_price = data.get('current_price')
#     if not symbol or not type_ or not date_str or not username:
#         return jsonify({'status': 'error', 'message': 'Missing required parameters'}), 400
#
#     result = create_recommend_stock(symbol, type_, date_str, price, username , current_price)
#     print(result)
#     return jsonify(result)
#
#
# @app.route('/api/stock/update-stock/<string:idRecommend>', methods=['PUT'])
# @swag_from({
#     'summary': 'Update a stock recommendation',
#     'description': 'This endpoint allows users to update the price, lastUpdate, and profit of a stock recommendation.',
#     'parameters': [
#         {
#             'name': 'idRecommend',
#             'in': 'path',
#             'type': 'string',
#             'required': True,
#             'description': 'The ID of the stock recommendation to update',
#             'example': 'some-unique-id'
#         },
#         {
#             'name': 'body',
#             'in': 'body',
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'price': {
#                         'type': 'integer',
#                         'description': 'The new purchase price of the stock',
#                         'example': 150
#                     },
#                     'date': {
#                         'type': 'string',
#                         'description': 'The new date for the stock recommendation in YYYY-MM-DD format',
#                         'example': '2024-09-27'
#                     },
#                     'current_price': {
#                         'type': 'integer',
#                         'description': 'The current price of the stock for profit calculation',
#                         'example': 200
#                     }
#                 },
#                 'required': ['price', 'date', 'current_price']
#             }
#         }
#     ],
#     'responses': {
#         '200': {
#             'description': 'Stock recommendation updated successfully',
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'status': {'type': 'string', 'example': 'success'},
#                     'message': {'type': 'string'}
#                 }
#             }
#         },
#         '404': {
#             'description': 'Recommendation not found',
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'status': {'type': 'string', 'example': 'error'},
#                     'message': {'type': 'string', 'example': 'Recommendation not found'}
#                 }
#             }
#         },
#         '400': {
#             'description': 'Missing required parameters',
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'status': {'type': 'string', 'example': 'error'},
#                     'message': {'type': 'string', 'example': 'Missing required parameters'}
#                 }
#             }
#         }
#     }
# })
# def update_stock():
#     data = request.get_json()
#
#     price = data.get('price')
#     date_str = data.get('date')
#     current_price = data.get('current_price')
#     name_symbol = request.args.get('symbol')
#     if not price or not date_str or not current_price:
#         return jsonify({'status': 'error', 'message': 'Missing required parameters'}), 400
#
#     result = update_recommend_stock(name_symbol, price, date_str, current_price)
#     return jsonify(result)

from flask import request, jsonify
from flasgger import swag_from

from trade import app
from trade.dao.stock import create_recommend_stock, update_recommend_stock, find_recommendation_by_symbol


@app.route('/api/stock/create-or-update-stock', methods=['POST'])
@swag_from({
    'summary': 'Create or update a stock recommendation',
    'description': 'This endpoint allows users to create a new stock recommendation or update an existing one by providing stock details such as symbol, type, date, price, and current price.',
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
                    'date': {
                        'type': 'string',
                        'description': 'The date for the stock recommendation in YYYY-MM-DD format',
                        'example': '2024-09-20'
                    },
                    'price': {
                        'type': 'integer',
                        'description': 'The purchase price of the stock',
                        'example': 150
                    },
                    'current_price': {
                        'type': 'integer',
                        'description': 'The current price of the stock for profit calculation',
                        'example': 200
                    }
                },
                'required': ['symbol', 'type', 'date', 'price', 'current_price']
            }
        },
        {
            'name': 'username',
            'in': 'query',
            'type': 'string',
            'description': 'The username of the user making the recommendation',
            'required': True,
            'example': 'john_doe'
        }
    ],
    'responses': {
        '200': {
            'description': 'Stock recommendation created or updated successfully',
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
                            'date': {'type': 'string'},
                            'price': {'type': 'integer'},
                            'current_price': {'type': 'integer'}
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
def create_or_update_stock():
    data = request.get_json()

    username = request.args.get('username')
    symbol = data.get('symbol')
    type_ = data.get('type')
    date_str = data.get('date')
    price = data.get('price')
    current_price = data.get('current_price')

    # Check for missing parameters
    if not symbol or not type_ or not date_str or not price or not current_price or not username:
        return jsonify({'status': 'error', 'message': 'Missing required parameters'}), 400

    # Check if the stock recommendation already exists
    existing_recommendation = find_recommendation_by_symbol(symbol)

    if existing_recommendation:
        # If it exists, update the recommendation
        result = update_recommend_stock(symbol, price, date_str, current_price)
        message = f"Stock recommendation for {symbol} updated successfully."
    else:
        # If it doesn't exist, create a new recommendation
        result = create_recommend_stock(symbol, type_, date_str, price, username, current_price)
        message = f"Stock recommendation for {symbol} created successfully."

    return jsonify({
        'status': 'success',
        'message': message,
        'data': result
    }), 200
