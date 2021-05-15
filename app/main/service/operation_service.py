from sqlalchemy import func

from app.main import db
from app.main.helper import utils
from app.main.helper.utils import create_response, get_side_id
from app.main.helper.validation_helper import valid_ticker
from app.main.model.operation import Operation
from app.main.model.user import User
from app.main.service import summary_service


def is_valid_operation(data):
    try:
        utils.get_side_id(data['side'])
        utils.get_date(data['date'])
    except:
        return False

    return valid_ticker(data['ticker']) and data['amount'] > 0 and data['price'] > 0


def save_new_operation(data):
    user = User.query.get(data['user_id'])
    if not user:
        return create_response('fail', 'User not found data.', 404)
    else:
        if not is_valid_operation(data):
            return create_response('fail', 'Invalid data.', 400)

        if get_side_id(data['side']) == get_side_id('sell'):
            remaining = compute_remaining_amount(data)
            if data['amount'] > remaining:
                return create_response('fail', 'You cannot sell more {} than you have.'.format(data['ticker']), 400)

        new_operation = Operation(
            ticker=data['ticker'],
            side=data['side'],
            amount=data['amount'],
            price=data['price'],
            date=data['date'],
            user=user)

        db.session.add(new_operation)
        db.session.commit()
        summary_service.update_position(data)
        return create_response('success', 'Operation successfully registered.', 201)


def __get_total_amount(data, side, is_update):
    if is_update:
        result = db.session.query(func.sum(Operation.amount)).filter(
            Operation.user_id == data['user_id'],
            Operation.ticker == data['ticker'],
            Operation.side_id == get_side_id(side),
            Operation.date <= data['date'],
            Operation.id != data['id']).scalar()
    else:
        result = db.session.query(func.sum(Operation.amount)).filter(
            Operation.user_id == data['user_id'],
            Operation.ticker == data['ticker'],
            Operation.side_id == get_side_id(side),
            Operation.date <= data['date']).scalar()

    return result if result else 0


def compute_remaining_amount(data, is_update=False):
    total_buy = __get_total_amount(data, side='buy', is_update=is_update)
    total_sell = __get_total_amount(data, side='sell', is_update=is_update)

    return total_buy - total_sell


def update_operation(data):
    operation = Operation.query.get(data['id'])
    if operation:
        if not is_valid_operation(data):
            return create_response('fail', 'Invalid data.', 400)

        if get_side_id(data['side']) == get_side_id('sell'):
            remaining = compute_remaining_amount(data, is_update=True)
            if data['amount'] > remaining:
                return create_response('fail', 'You cannot sell more {} than you have.'.format(data['ticker']), 400)

        operation.ticker = data['ticker']
        operation.side = data['side']
        operation.amount = data['amount']
        operation.price = data['price']
        operation.date = data['date']
        db.session.commit()
        summary_service.update_position(data)
        return operation
    else:
        return create_response('fail', 'Operation not found.', 404)


def delete_operation(data):
    operation = db.session.query(Operation).filter(Operation.id == data['id']).first()
    if operation:
        summary_service.update_position(data)
        db.session.delete(operation)
        db.session.commit()
        summary_service.update_position(data)
        return create_response('success', 'Operation successfully deleted.', 204)
    else:
        return create_response('fail', 'Operation not found.', 404)


def filter_operation(data):
    query = db.session.query(Operation).filter_by(user_id=data['user_id'])
    if data.get('ticker', None):
        query = query.filter_by(_ticker=data['ticker'])
    if data.get('date', None):
        query = query.filter_by(_date=data['date'])
    return query.all()
