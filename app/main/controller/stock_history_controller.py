from flask import request
from flask_restx import Resource

from app.main.dto.stock_hist_dto import StockHistDto
from app.main.service.stock_history_service import update_historical_data

api = StockHistDto.api

# TODO WIP API, this will probably be replaced by apis that retrieve consolidated info for wallets


@api.route('/')
class StockHistory(Resource):
    @api.response(201, 'Stocks successfully retrieved')
    @api.doc('Fetch all available stocks in the system.')
    def get(self):
        """Fetches data for tickers"""
        tickers = request.args.get('tickers').split(',')
        return update_historical_data(tickers)
