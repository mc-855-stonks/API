from flask_restx import Resource

from app.main.dto.stock_dto import StockDto
from app.main.service.stock_service import get_available_stocks

api = StockDto.api

# WIP API, this will probably be replaced by apis that retrieve consolidated info for wallets


@api.route('/')
class StockInfo(Resource):
    @api.response(201, 'Stocks successfully retrieved')
    @api.doc('Fetch all available stocks in the system.')
    def get(self):
        """Fetches data for tickers"""
        return get_available_stocks()
