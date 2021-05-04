from flask import request
from flask_restx import Resource, marshal

from app.main.dto.operation_dto import OperationDto
from app.main.helper.decorator import token_required
from app.main.service.auth_service import Auth
from app.main.service.operation_service import save_new_operation, update_operation, delete_operation, filter_operation

api = OperationDto.api


@api.route('/')
class Operation(Resource):
    @api.response(201, 'Operation successfully created.')
    @api.doc('Create a new operation.')
    @api.expect(OperationDto.post_operation, validate=True)
    @token_required
    def post(self):
        """Creates a new Operation """
        data = request.json
        response, status = Auth.get_logged_in_user(request)
        user_id = response.get('data').get('user_id')
        data['user_id'] = user_id
        return save_new_operation(data=data)

    @api.doc('Update operation data. Token Authentication is Required.')
    @api.expect(OperationDto.put_operation, validate=True)
    @token_required
    def put(self):
        """Update operation data"""
        data = request.json
        response, status = Auth.get_logged_in_user(request)
        user_id = response.get('data').get('user_id')
        data['user_id'] = user_id
        operation = update_operation(data=data)
        if isinstance(operation, tuple) and operation[0].get('status', None) == 'fail':
            return operation

        return marshal(operation, OperationDto.put_operation, envelope='data')

    @api.response(204, 'Operation successfully deleted.')
    @api.doc('Delete operation data. Token Authentication is Required.')
    @api.expect(OperationDto.delete_operation, validate=True)
    @token_required
    def delete(self):
        """Delete operation data"""
        data = request.json
        return delete_operation(data=data)

    @api.doc('Get operation data. Token Authentication is Required.')
    @api.marshal_list_with(OperationDto.get_operation, envelope='data')
    @token_required
    def get(self):
        """Get operation data"""
        response, status = Auth.get_logged_in_user(request)
        user_id = response.get('data').get('user_id')
        data = {'user_id': user_id}
        ticker = request.args.get('ticker')
        date = request.args.get('date')

        if ticker:
            data['ticker'] = ticker
        if date:
            data['date'] = date

        return filter_operation(data=data)
