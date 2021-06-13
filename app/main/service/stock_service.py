from app.main import db
from app.main.model.stock import Stock


def get_available_stocks():
    return db.session.query(Stock).all()


def check_tickers_exists(tickers):
    if type(tickers) != list:
        tickers = [tickers]

    valid_stock_ids = []
    for ticker in tickers:
        stock = Stock.query.filter_by(_ticker=ticker.upper()).first()
        if not stock:
            return False, valid_stock_ids
        else:
            valid_stock_ids.append(stock.id)

    return True, valid_stock_ids
