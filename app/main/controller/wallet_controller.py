from flask import request
from flask_restx import Resource

from app.main.dto.wallet_dto import WalletDto
from app.main.helper.decorator import token_required
from app.main.service.auth_service import Auth
from app.main.service.summary_service import get_wallet_summary

api = WalletDto.api

@api.route('/')
class Wallet(Resource):
    @api.doc('Get the wallet summary. Token Authentication is Required.')
    @token_required
    def get(self):
        """Get operation data"""
        response, status = Auth.get_logged_in_user(request)
        user_id = response.get('data').get('user_id')
        result = get_wallet_summary(user_id)
        return result
