from flask_restx import Namespace, fields


class WalletDto:
    api = Namespace('wallet', description='Wallet related operations')
    # wallet = api.model('wallet', {
    #     'date': fields.Date(required=True, description='date'),
    #     'side': fields.String(required=True, description='operation side'),
    #     'amount': fields.Integer(required=True, description='amount'),
    #     'price': fields.Float(required=True, description='price'),
    #     'ticker': fields.String(required=True, description='ticker'),
    # })
