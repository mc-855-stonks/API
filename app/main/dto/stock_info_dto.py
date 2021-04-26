from flask_restx import Namespace, fields

class StockInfoDto:
    api = Namespace('stockinfo', description='retrieving api informations for tickers')
    stock_tickers = api.model('stockTickers', {
        'tickers': fields.List(fields.String, required=True, description='Array of stock tickers'),
    })
