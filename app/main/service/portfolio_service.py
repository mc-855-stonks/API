from app.main import db
from app.main.helper.utils import create_response
from app.main.model.summary import Summary
from app.main.model.user import User
from app.main.service.summary_service import get_current_stock_info


def compute_portfolio(user_id):
    user = User.query.get(user_id)

    if not user:
        return create_response('fail', 'User not found data.', 404)
    else:
        wallet_summary = db.session.query(Summary).filter_by(user_id=user_id).all()
        stock_response, status = get_current_stock_info(wallet_summary)
        if status != 200 and stock_response.get('status', None) == 'fail':
            return stock_response, status

        portfolio_total = 0
        stocks = []
        for summary in wallet_summary:
            curr_price = stock_response[summary.stock.ticker]["previousClose"]
            if isinstance(curr_price, dict) and curr_price.get('raw', None):
                curr_price = curr_price['raw']

            curr_total = summary.amount * curr_price
            portfolio_total += curr_total

            result_stock_info = {'ticker': summary.stock.ticker,
                                 'sector': summary.stock.sector,
                                 'current_total': curr_total}
            stocks.append(result_stock_info)

        for stock in stocks:
            stock['proportion'] = stock['current_total'] / portfolio_total

        return {"stocks": stocks}


def get_current_portfolio(user_id, groupby='ticker'):
    result = compute_portfolio(user_id)
    if groupby == 'ticker':
        return result
    elif groupby == 'sector':
        sectors = {}
        for stock in result['stocks']:
            sector = stock['sector']
            sector_data = sectors.get(sector, {'sector': sector,
                                               'current_total': 0,
                                               'proportion': 0})

            sector_data['current_total'] += stock['current_total']
            sector_data['proportion'] += stock['proportion']
            sectors[sector] = sector_data
        return {'sectors': list(sectors.values())}
    else:
        return create_response('fail', 'groupby can not be {}'.format(groupby), 400)
