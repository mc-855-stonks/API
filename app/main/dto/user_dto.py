from flask_restx import Namespace, fields


class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'id': fields.Integer(required=False, description='user id'),
        'name': fields.String(required=False, description='user username'),
        'email': fields.String(required=False, description='user email address'),
        'password': fields.String(required=False, description='user password'),
        'investor_profile': fields.String(required=False, description='user investment profile'),
    })
