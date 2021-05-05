from flask import request
from flask_restx import Resource, marshal

from app.main.dto.user_dto import UserDto
from app.main.helper.decorator import token_required
from app.main.service.auth_service import Auth
from app.main.service.user_service import save_new_user, update_user, get_user_by_id
from flask_cors import cross_origin

api = UserDto.api
user_fields = UserDto.user

@api.route('/')
class UserList(Resource):
    @api.response(201, 'User successfully created.')
    @api.doc('Create a new user.')
    @api.expect(user_fields, validate=True)
    def post(self):
        """Creates a new User """
        data = request.json
        return save_new_user(data=data)

    @api.response(200, 'User successfully updated.')
    @api.doc('Update user data. Token Authentication is Required.')
    @api.expect(user_fields, validate=True)
    @token_required
    @cross_origin(allow_headers='Authorization, Content-Type')
    def put(self):
        """Update user data"""
        data = request.json
        response, status = Auth.get_logged_in_user(request)
        user_id = response.get('data').get('user_id')
        data['id'] = user_id
        return update_user(data=data)

    @api.doc('Get user data. Token Authentication is Required.')
    @token_required
    def get(self):
        """get user data given its id"""
        response, status = Auth.get_logged_in_user(request)
        user_id = response.get('data').get('user_id')
        user = get_user_by_id(user_id)
        if isinstance(user, tuple) and user[0].get('status', None) == 'fail':
            api.abort(404, "User '{}' not found.".format(user_id))
        else:
            return marshal(user, user_fields, envelope='data')
