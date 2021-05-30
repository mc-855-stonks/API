from flask_restx import Namespace, fields


class StockHistDto:
    api = Namespace('stock_hist', description='retrieve available stocks')
