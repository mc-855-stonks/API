from datetime import datetime

from app.main import db


class StockHistory(db.Model):
    """
    Stock History Model for storing historical data
    """
    __tablename__ = 'stock_history'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    open = db.Column(db.Float, nullable=False)
    high = db.Column(db.Float, nullable=False)
    low = db.Column(db.Float, nullable=False)
    close = db.Column(db.Float, nullable=False)
    volume = db.Column(db.BigInteger, nullable=False)
    date = db.Column(db.Date, nullable=False)

    last_update_date = db.Column(db.Date, nullable=False, default=datetime.now())
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'))
    stock = db.relationship("Stock", back_populates='stock_history')

    @property
    def ticker(self):
        return self.stock.ticker

    def get_dict(self):
        return {'id': self.id,
                'open': self.open,
                'close': self.close,
                'high': self.high,
                'low': self.low,
                'volume': self.volume,
                'date': self.date}

    def __repr__(self):
        return '<stock({}): date: {}, ticker: {}, close: {}'.format(self.id, self.date, self.ticker, self.close)