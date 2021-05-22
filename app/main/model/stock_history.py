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