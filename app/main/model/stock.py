from app.main import db


class Stock(db.Model):
    """
    Infos about the available stocks in the system
    """
    __tablename__ = 'stock'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Unicode, nullable=True)
    _ticker = db.Column(db.Unicode, nullable=True)
    sector = db.Column(db.Unicode, nullable=True)
    image = db.Column(db.Unicode, nullable=True)
    operation = db.relationship("Operation", back_populates='stock')
    summary = db.relationship("Summary", back_populates='stock')
    stock_history = db.relationship("StockHistory", back_populates='stock')

    @property
    def ticker(self):
        return self._ticker.upper()

    @ticker.setter
    def ticker(self, ticker):
        self._ticker = ticker.upper()

    def __repr__(self):
        return '<stock({}): name: {}, ticker: {}'.format(self.id, self.name, self.ticker)
