from app.main import db
from app.main.helper.utils import create_response, compute_mean_price_amount, get_side_id, format_monetary_value, \
    format_percentage
from app.main.model.operation import Operation
from app.main.model.summary import Summary
from app.main.model.user import User
from app.main.service.stock_info_service import StockInfoService


def update_position(data):
    user = User.query.get(data['user_id'])

    if not user:
        return create_response('fail', 'User not found data.', 404)
    else:
        operations = db.session.query(Operation).filter_by(user_id=data['user_id']) \
            .filter_by(_ticker=data['ticker'].upper()).all()

        operations = [(op.price, op.amount) if op.side_id == get_side_id('buy') else (op.price, -op.amount) for op in operations]
        mean_price, amount = compute_mean_price_amount(operations)

        summary = Summary.query.filter_by(user_id=data['user_id']) \
            .filter_by(_ticker=data['ticker'].upper()) \
            .first()

        # opening the position
        if not summary:
            new_summary = Summary(
                ticker=data['ticker'],
                amount=amount,
                mean_price=mean_price,
                user=user)
            db.session.add(new_summary)
        else:
            # closing the position
            if summary.amount == amount:
                db.session.delete(summary)
            else:
                # updating the position
                summary.amount = amount
                summary.mean_price = mean_price

        db.session.commit()
        return create_response('success', 'Position successfully updated.', 201)


def get_wallet_summary(user_id):
    user = User.query.get(user_id)

    if not user:
        return create_response('fail', 'User not found data.', 404)
    else:
        wallet_summary = db.session.query(Summary).filter_by(user_id=user_id).all()
        tickers = [summary.ticker for summary in wallet_summary]
        stock_response, status = StockInfoService.get_stock_info(data={'tickers': tickers})
        if status != 200 and stock_response.get('status', None) == 'fail':
            return create_response('fail', 'Stock info can not be retrieved.', 500)

        total_invested = 0
        wallet_total = 0
        stocks = []
        for summary in wallet_summary:
            curr_price = stock_response[summary.ticker]["previousClose"]
            if isinstance(curr_price, dict) and curr_price.get('raw', None):
                curr_price = curr_price['raw']

            company_name = stock_response[summary.ticker]["shortName"]
            invested = summary.amount * summary.mean_price
            curr_total = summary.amount * curr_price
            curr_return = curr_total - invested
            curr_return_percent = 100 * (curr_total - invested) / invested

            total_invested += invested
            wallet_total += curr_total

            result_stock_info = {'ticker': summary.ticker,
                                 'company_name': company_name,
                                 'invested_value': format_monetary_value(invested),
                                 'current_total': format_monetary_value(curr_total),
                                 'current_price': format_monetary_value(curr_price),
                                 'mean_price': format_monetary_value(summary.mean_price),
                                 'curr_return': format_monetary_value(curr_return),
                                 'curr_return_percent': format_percentage(curr_return_percent),
                                 'amount': summary.amount}
            stocks.append(result_stock_info)

        wallet_return = wallet_total - total_invested
        wallet_return_percent = 100 * (wallet_total - total_invested) / total_invested

        return {"total_invested": format_monetary_value(total_invested),
                "wallet_total": format_monetary_value(wallet_total),
                "wallet_return": format_monetary_value(wallet_return),
                "wallet_return_percent": format_percentage(wallet_return_percent),
                "stocks": stocks}