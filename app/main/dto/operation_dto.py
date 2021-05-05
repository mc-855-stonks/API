from flask_restx import Namespace, fields


class OperationDto:
    api = Namespace('operation', description='Operation related operations')
    post_operation = api.model('post_operation', {
        'date': fields.Date(required=True, description='date'),
        'side': fields.String(required=True, description='operation side'),
        'amount': fields.Integer(required=True, description='amount'),
        'price': fields.Float(required=True, description='price'),
        'ticker': fields.String(required=True, description='ticker'),
    })

    put_operation = api.model('put_operation', {
        'id': fields.Integer(required=True, description='operation id'),
        'date': fields.Date(required=True, description='date'),
        'side': fields.String(required=True, description='operation side'),
        'amount': fields.Integer(required=True, description='amount'),
        'price': fields.Float(required=True, description='price'),
        'ticker': fields.String(required=True, description='ticker'),
    })

    get_operation = api.model('get_operation', {
        'id': fields.Integer(required=True, description='operation id'),
        'date': fields.Date(required=True, description='date'),
        'side': fields.String(required=True, description='operation side'),
        'amount': fields.Integer(required=True, description='amount'),
        'price': fields.Float(required=True, description='price'),
        'ticker': fields.String(required=True, description='ticker'),
    })

    delete_operation = api.model('delete_operation', {
        'id': fields.Integer(required=True, description='operation id'),
    })
