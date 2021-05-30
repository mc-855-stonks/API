import json

import yfinance as yf

from app.main.helper.redis import redis
from app.main.helper.utils import create_response

STOCKS_REDIS_PREFIX = "stock:"
TTL_STOCKS = 60 * 10 # 10 minutes

class StockInfoService:
    @staticmethod
    def get_stock_info(data):
        try:
            tickers = data.get('tickers')
            tickers_to_refresh = []
            response = {}
            for ticker in tickers:
                ticker = ticker.upper()
                ticker_info = redis.get(STOCKS_REDIS_PREFIX + ticker)
                if ticker_info:
                    try:
                        ticker_info = ticker_info.decode('utf8')
                    except (UnicodeDecodeError, AttributeError):
                        pass

                    response[ticker] = json.loads(ticker_info)
                else:
                    tickers_to_refresh.append(ticker)
            ticker_names = [ticker + ".SA" for ticker in tickers_to_refresh]
            ticker_data = yf.Tickers(" ".join(ticker_names))

            for ticker in tickers_to_refresh:
                info = ticker_data.tickers[ticker + ".SA"].info
                redis.set(STOCKS_REDIS_PREFIX + ticker, json.dumps(info), ex=TTL_STOCKS)
                response[ticker] = info

            return response, 200
        except Exception as e:
            print(e)
            return create_response('fail', 'Unexpected Error. Try again.', 500)
