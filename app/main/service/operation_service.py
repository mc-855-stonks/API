from sqlalchemy import func


from app.main import db
from app.main.helper import utils, date_helper
from app.main.helper.utils import create_response, get_side_id
from app.main.helper.validation_helper import valid_ticker
from app.main.model.operation import Operation
from app.main.model.stock import Stock
from app.main.model.user import User
from app.main.service import summary_service


def is_valid_operation(data):
    try:
        utils.get_side_id(data['side'])
        date_helper.str_to_date(data['date'])
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

        stock = Stock.query.filter_by(_ticker=data['ticker'].upper()).first()
        if not stock:
            return create_response('fail', 'Invalid ticker.', 400)

        if get_side_id(data['side']) == get_side_id('sell'):
            remaining = compute_remaining_amount(data, stock=stock)
            if data['amount'] > remaining:
                return create_response('fail', 'You cannot sell more {} than you have.'.format(data['ticker']), 400)

        new_operation = Operation(
            side=data['side'],
            amount=data['amount'],
            price=data['price'],
            date=data['date'],
            user=user,
            stock=stock)

        db.session.add(new_operation)
        db.session.commit()
        summary_service.update_position(data)
        return create_response('success', 'Operation successfully registered.', 201)


def __get_total_amount(data, side, stock, is_update):
    if is_update:
        result = db.session.query(func.sum(Operation.amount)).filter(
            Operation.user_id == data['user_id'],
            Operation.stock_id == stock.id,
            Operation.side_id == get_side_id(side),
            Operation._date <= data['date'],
            Operation.id != data['id']).scalar()
    else:
        result = db.session.query(func.sum(Operation.amount)).filter(
            Operation.user_id == data['user_id'],
            Operation.stock_id == stock.id,
            Operation.side_id == get_side_id(side),
            Operation._date <= data['date']).scalar()

    return result if result else 0


def compute_remaining_amount(data, stock, is_update=False):
    total_buy = __get_total_amount(
        data, side='buy', stock=stock, is_update=is_update)
    total_sell = __get_total_amount(
        data, side='sell', stock=stock, is_update=is_update)

    return total_buy - total_sell


def update_operation(data):
    operation = Operation.query.get(data['id'])
    if operation:
        if not is_valid_operation(data):
            return create_response('fail', 'Invalid data.', 400)

        stock = Stock.query.filter_by(_ticker=data['ticker'].upper()).first()
        if not stock:
            return create_response('fail', 'Invalid ticker.', 400)

        if get_side_id(data['side']) == get_side_id('sell'):
            remaining = compute_remaining_amount(
                data, stock=stock, is_update=True)
            if data['amount'] > remaining:
                return create_response('fail', 'You cannot sell more {} than you have.'.format(data['ticker']), 400)

        prev_stock = operation.stock
        operation.stock = stock
        operation.side = data['side']
        operation.amount = data['amount']
        operation.price = data['price']
        operation.date = data['date']
        db.session.commit()
        summary_service.update_position(data)
        if prev_stock != stock:
            summary_service.update_position(
                {'user_id': data['user_id'], 'ticker': prev_stock.ticker})
        return operation
    else:
        return create_response('fail', 'Operation not found.', 404)


def delete_operation(data):
    operation = db.session.query(Operation).filter(
        Operation.id == data['id']).first()
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
        stock = Stock.query.filter_by(_ticker=data['ticker'].upper()).first()
        if not stock:
            return create_response('fail', 'Invalid ticker.', 400)

        query = query.filter_by(stock_id=stock.id)
    if data.get('date', None):
        query = query.filter_by(_date=data['date'])

    if data.get('since', None):
        query = query.filter(Operation._date >= data['since'])

    return query.all()


