from flask_restx import Namespace, fields


class StockDto:
    api = Namespace('stock', description='retrieve available stocks')
    stock = api.model('stock', {
        'name': fields.String(required=False, description='stock name'),
        'ticker': fields.String(required=False, description='ticker'),
        'segment': fields.String(required=False, description='company segment'),
        'image': fields.String(required=False, description='image'),
    })
