from flask import request
from flask_cors import cross_origin
from flask_restx import Resource

from app.main.dto.portfolio_performance_dto import PortfolioPerformanceDto
from app.main.helper.decorator import token_required
from app.main.helper.utils import create_response
from app.main.service.auth_service import Auth
from app.main.service.portfolio_performance_services import get_portfolio_daily_returns, \
    get_portfolio_monthly_returns

api = PortfolioPerformanceDto.api

@api.route('/')
class PortfolioPerformance(Resource):
    @api.doc('Get the portfolio performance metrics. Token Authentication is Required.')
    @token_required
    @cross_origin(allow_headers='Authorization, Content-Type')
    def get(self):
        """Get the portfolio performance metrics. Use the parameter 'months' to indicate how long you
        want to analyze the portfolio performance, by default we use months=12;
        Token Authentication is Required."""

        response, status = Auth.get_logged_in_user(request)
        user_id = response.get('data').get('user_id')
        months = request.args.get('months', default=12)
        if months < 1:
            return create_response('fail', 'Parameter ``months´´ must be at least 1.', 400)

        df_returns = get_portfolio_daily_returns(user_id=user_id, n_months=months)
        returns = get_portfolio_monthly_returns(df_returns)
        return {'returns': returns}