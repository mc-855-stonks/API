from flask import request
from flask_restx import Resource

from app.main.dto.user_dto import UserDto
from app.main.service.user import get_all_users, save_new_user, get_a_user

api = UserDto.api
_user = UserDto.user

@api.route('/')
class UserList(Resource):
    @api.doc('list registered users')
    @api.marshal_list_with(_user, envelope='data')
    def get(self):
        """List all registered users"""
        return get_all_users()

    @api.response(201, 'User successfully created.')
    @api.doc('create a new user')
    @api.expect(_user, validate=True)
    def post(self):
        """Creates a new User """
        data = request.json
        return save_new_user(data=data)


@api.route('/<string:username>')
@api.param('username', 'The username')
class User(Resource):
    @api.doc('get a user')
    @api.marshal_with(_user)
    def get(self, username):
        """get a user given its username"""
        user = get_a_user(username)
        if not user:
            api.abort(404, "User '{}' not found.".format(username))
        else:
            return user