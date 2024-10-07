import uuid


from trade import db
from trade.model import  User, SignalBuy, SignalSell


def calculate_profit(current_price, purchase_price):
    if purchase_price == 0:
        return 0
    return ((current_price - purchase_price) / purchase_price) * 100


def create_recommend_stock(symbol, type_, date_str, price, username, current_price, interval, resolution):
    try:
        user = User.query.filter_by(username=username).first()
        if not user:
            return {'status': 'error', 'message': 'User not found'}, 404

        print(type_)

        if type_ == 1:
            # Tạo tín hiệu mua
            id_signal_buy = str(uuid.uuid4())
            profit = calculate_profit(current_price, price)

            new_signal_buy = SignalBuy(
                id=id_signal_buy,
                stock=symbol,
                last_update=date_str,
                last_price=price,
                price_recommend=current_price,
                profit=profit,
                buy_time=date_str,
                interval=interval,
                resolution=resolution
            )
            db.session.add(new_signal_buy)
            db.session.commit()

            return {'status': 'success', 'message': 'Buy signal created successfully', 'id': id_signal_buy}

        elif type_ == 2:
            last_buy_signal = SignalBuy.query.filter_by(stock=symbol).order_by(SignalBuy.buy_time.desc()).first()
            print(f"last buy signal: {last_buy_signal}")
            if not last_buy_signal:
                return {'status': 'error',
                        'message': 'No Buy signal found for this stock to associate with Sell signal'}, 404

            existing_sell_signal = SignalSell.query.filter_by(buy_id=last_buy_signal.id).first()
            if existing_sell_signal:
                return {'status': 'error', 'message': 'This Buy signal has already been sold'}, 400

            # Tạo tín hiệu bán nếu chưa có tín hiệu bán
            id_signal_sell = str(uuid.uuid4())
            profit = calculate_profit(price, last_buy_signal.price_recommend)
            new_signal_sell = SignalSell(
                id=id_signal_sell,
                stock=symbol,
                recommend=last_buy_signal.price_recommend,
                price=price,
                buy_time=last_buy_signal.buy_time,
                sell_time=date_str,
                buy_id=last_buy_signal.id,
                profit=profit,
                interval=interval,
                resolution=resolution
            )
            db.session.add(new_signal_sell)
            db.session.commit()

            return {'status': 'success', 'message': 'Sell signal created successfully', 'id': id_signal_sell}

    except Exception as e:
        print(str(e))
        db.session.rollback()
        return {'status': 'error', 'message': str(e)}


def update_recommend_stock(id_recommend, new_price, date_str):
    try:
        recommendation = SignalBuy.query.filter_by(id=id_recommend).first()
        print(recommendation)
        if not recommendation:
            return {'status': 'error', 'message': 'Recommendation not found'}, 404
        print(date_str)
        print(new_price)
        recommendation.last_price = new_price
        recommendation.last_update = date_str
        recommendation.profit = calculate_profit(new_price, recommendation.price_recommend)

        db.session.commit()
        print("Stock recommendation updated successfully")
        return {'status': 'success', 'message': 'Stock recommendation updated successfully'}

    except Exception as e:
        db.session.rollback()
        print(str(e))
        return {'status': 'error', 'message': str(e)}


def find_recommendation_by_symbol(symbol):

     return SignalBuy.query.filter_by(stock=symbol).first()