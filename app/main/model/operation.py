import datetime

from app.main.helper import date_helper
from app.main import db
from app.main.helper import utils


class Operation(db.Model):
    """
    Operation Model for storing stock buy/sell operations
    """
    __tablename__ = 'operation'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    side_id = db.Column(db.SmallInteger, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    _date = db.Column(db.Date, nullable=False, default=datetime.datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates='operation')
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'))
    stock = db.relationship("Stock", back_populates='operation')

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, str_date):
        self._date = date_helper.str_to_date(str_date)

    @property
    def side(self):
        return utils.get_side(self.side_id)

    @side.setter
    def side(self, side):
        self.side_id = utils.get_side_id(side)

    @property
    def ticker(self):
        return self.stock.ticker

    def get_dict(self):
        return {'id': self.id,
                'side': self.side,
                'ticker': self.ticker,
                'amount': self.amount,
                'price': self.price,
                'date': self.date}

    def __repr__(self):
        return '<operation({}): {} [{}] - price: {}, amount: {}, date: {}'.format(self.id, self.stock.ticker, self.side,
                                                                                  self.price, self.amount, self.date)
