from flask import request
from flask_restx import Resource, marshal

from app.main.dto.stock_info_dto import StockInfoDto
from app.main.service.stock_info_service import StockInfoService

api = StockInfoDto.api
stock_tickers = StockInfoDto.stock_tickers

# WIP API, this will probably be replaced by apis that retrieve consolidated info for wallets
@api.route('/stockinfo')
class StockInfo(Resource):
    @api.response(201, 'Stocks info successfully retrieved')
    @api.doc('Fetch market data for passed tickers.')
    @api.expect(stock_tickers, validate=True)
    def post(self):
        """Fetches data for tickers"""
        data = request.json
        return StockInfoService.get_stock_info(data=data)