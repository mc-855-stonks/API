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

    # @api.response(200, 'User successfully updated.')
    # @api.doc('Update user data. Token Authentication is Required.')
    # @api.expect(user_fields, validate=True)
    # @token_required
    # def put(self):
    #     """Update user data"""
    #     data = request.json
    #     response, status = Auth.get_logged_in_user(request)
    #     user_id = response.get('data').get('user_id')
    #     data['id'] = user_id
    #     return update_user(data=data)

    # @api.doc('Get user data. Token Authentication is Required.')
    # @token_required
    # def get(self):
    #     """get user data given its id"""
    #     response, status = Auth.get_logged_in_user(request)
    #     user_id = response.get('data').get('user_id')
    #     user = get_user_by_id(user_id)
    #     if isinstance(user, tuple) and user[0].get('status', None) == 'fail':
    #         api.abort(404, "User '{}' not found.".format(user_id))
    #     else:
    #         return marshal(user, user_fields, envelope='data')
