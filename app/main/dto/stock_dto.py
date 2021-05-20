from flask_restx import Namespace

class StockDto:
    api = Namespace('stock', description='retrieve available stocks')