from app.main import db


class Summary(db.Model):
    """
    Summary Model for storing the summary of a wallet
    """
    __tablename__ = 'summary'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    amount = db.Column(db.Integer, nullable=False)
    mean_price = db.Column(db.Float, nullable=False)
    _ticker = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates='summary')

    @property
    def ticker(self):
        return self._ticker.upper()

    @ticker.setter
    def ticker(self, ticker):
        self._ticker = ticker.upper()

    def __repr__(self):
        return '<operation({}): price: {}, amount: {}'.format(self.id, self.ticker, self.mean_price, self.amount)
