from app.main import db


class Summary(db.Model):
    """
    Summary Model for storing the summary of a wallet
    """
    __tablename__ = 'summary'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    amount = db.Column(db.Integer, nullable=False)
    mean_price = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates='summary')
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'))
    stock = db.relationship("Stock", back_populates='summary')


    def __repr__(self):
        return '<wallet({}): price: {}, amount: {}'.format(self.id, self.stock.ticker, self.mean_price, self.amount)
