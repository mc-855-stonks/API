from flask import request
from flask_restx import Resource

from app.main.dto.portfolio_dto import PortfolioDto
from app.main.helper.decorator import token_required
from app.main.service.auth_service import Auth
from app.main.service.portfolio_service import get_current_portfolio

api = PortfolioDto.api

@api.route('/')
class Portfolio(Resource):
    @api.doc('Get the portfolio data. Token Authentication is Required.')
    # @token_required
    def get(self):
        """Get operation data"""
        # response, status = Auth.get_logged_in_user(request)
        # user_id = response.get('data').get('user_id')
        user_id = 1
        group_by = request.args.get('groupby')
        result = get_current_portfolio(user_id, groupby=group_by)
        return result
