from flask import request
from flask_cors import cross_origin
from flask_restx import Resource

from app.main.dto.portfolio_performance_dto import PortfolioPerformanceDto
from app.main.helper.decorator import token_required
from app.main.service.auth_service import Auth
from app.main.service.portfolio_performance_services import get_performance_metrics

api = PortfolioPerformanceDto.api

@api.route('/')
class PortfolioPerformance(Resource):
    @api.doc('Get the portfolio performance metrics. Token Authentication is Required.')
    @token_required
    @cross_origin(allow_headers='Authorization, Content-Type')
    def get(self):
        """Get the portfolio performance metrics. Use the parameter 'months' to indicate how long you
        want to analyze the portfolio performance metrics, by default we use months=12;
        Token Authentication is Required."""

        response, status = Auth.get_logged_in_user(request)
        user_id = response.get('data').get('user_id')
        return get_performance_metrics(user_id, n_months=3)
