from flask import request
from flask_cors import cross_origin
from flask_restx import Resource

from app.main.dto.portfolio_return_dto import PortfolioReturnDto
from app.main.helper.decorator import token_required
from app.main.helper.utils import create_response
from app.main.service.auth_service import Auth
from app.main.service.portfolio_return_services import get_portfolio_daily_returns, \
    get_portfolio_monthly_returns, get_portfolio_last_day_returns

api = PortfolioReturnDto.api


@api.route('/')
class PortfolioReturn(Resource):
    @api.doc('Get the portfolio return. Token Authentication is Required.')
    @token_required
    @cross_origin(allow_headers='Authorization, Content-Type')
    def get(self):
        """Get the portfolio return. Use the parameter 'months' to indicate how long you
        want to analyze the portfolio, by default we use months=12;
        Token Authentication is Required."""

        response, status = Auth.get_logged_in_user(request)
        user_id = response.get('data').get('user_id')
        months = request.args.get('months', default=12)
        if months < 1:
            return create_response('fail', 'Parameter ``months´´ must be at least 1.', 400)

        df_returns = get_portfolio_daily_returns(
            user_id=user_id, n_months=months)
        returns = get_portfolio_monthly_returns(df_returns)
        return {'returns': returns}

    @api.doc('Get the last day portifolio return. Token Authentication is Required.')
    @token_required
    @api.route('/daily')
    @cross_origin(allow_headers='Authorization, Content-Type')
    def get(self):
        """Get the portfolio return for the last day.
        Token Authentication is Required."""

        response, status = Auth.get_logged_in_user(request)
        user_id = response.get('data').get('user_id')

        df_returns = get_portfolio_daily_returns(user_id=user_id, n_months=1)
        returns = get_portfolio_last_day_returns(df_returns)
        return {'returns': returns}
