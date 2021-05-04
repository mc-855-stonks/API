import datetime

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
    ticker = db.Column(db.String(10), nullable=False)
    _date = db.Column(db.Date, nullable=False, default=datetime.datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates='operations')

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, str_date):
        self._date = utils.get_date(str_date)

    @property
    def side(self):
        return utils.get_side(self.side_id)

    @side.setter
    def side(self, side):
        self.side_id = utils.get_side_id(side)

    def __repr__(self):
        return '<operation({}): {} [{}] - price: {}, amount: {}, date: {}'.format(self.id, self.ticker, self.side,
                                                                                  self.price, self.amount, self.date)
