from flask_restx import Namespace, fields


class StockDto:
    api = Namespace('stock', description='retrieve available stocks')
    stock = api.model('stock', {
        'id': fields.Integer(required=False, description='stock id'),
        'name': fields.String(required=False, description='stock name'),
        'ticker': fields.String(required=False, description='ticker'),
        'segment': fields.String(required=False, description='company segment'),
        'image': fields.String(required=False, description='image'),
    })
