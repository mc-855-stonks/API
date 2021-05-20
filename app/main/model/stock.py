from app.main import db


class Stock(db.Model):
    """
    Infos about the available stocks in the system
    """
    __tablename__ = 'stock'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Unicode, nullable=True)
    ticker = db.Column(db.Unicode, nullable=True)
    segment = db.Column(db.Unicode, nullable=True)
    image = db.Column(db.Unicode, nullable=True)

    def __repr__(self):
        return '<stock({}): name: {}, ticker: {}'.format(self.id, self.name, self.ticker)
