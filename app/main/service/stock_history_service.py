import yfinance as yf

from app.main.helper.utils import create_response
from app.main.model.stock import Stock
from app.main.model.stock_history import StockHistory
from app.main import db


def get_historical_data(tickers, period='1y'):
    tickers = [ticker.upper() + ".SA" for ticker in tickers]
    stock_data = yf.Tickers(tickers)
    result = {}
    for ticker, data in stock_data.tickers.items():
        hist = data.history(period=period)
        result[ticker.split('.SA')[0]] = hist
    return result


def delete_historical_data(stock):
    db.session.query(StockHistory).filter(StockHistory.stock_id == stock.id).delete(synchronize_session=False)
    db.session.commit()


def update_historical_data(tickers):
    historical_data = get_historical_data(tickers)
    for ticker, data in historical_data.items():
        stock = Stock.query.filter_by(_ticker=ticker.upper()).first()
        if not stock:
            return create_response('fail', 'Invalid ticker {}.'.format(ticker), 400)
        delete_historical_data(stock=stock)

        history = []
        for row in data.iterrows():
            history.append(StockHistory(open=row[1]['Open'], close=row[1]['Close'],
                                        high=row[1]['High'], low=row[1]['Low'],
                                        volume=row[1]['Volume'], date=row[0],
                                        stock=stock))
        db.session.add_all(history)
        db.session.commit()

