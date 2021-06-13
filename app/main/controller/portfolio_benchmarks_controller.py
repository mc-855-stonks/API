from flask import request
from flask_cors import cross_origin
from flask_restx import Resource

from app.main.dto.portfolio_benchmarks_dto import PortfolioBenchmarksDto
from app.main.helper.decorator import token_required
from app.main.helper.utils import create_response
from app.main.service.auth_service import Auth
from app.main.service.benchmark_service import get_portfolio_benchmarks

api = PortfolioBenchmarksDto.api

@api.route('/')
class PortfolioBenchmarks(Resource):
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

        data = get_portfolio_benchmarks(user_id=user_id, n_months=months)
        return {'data': data}