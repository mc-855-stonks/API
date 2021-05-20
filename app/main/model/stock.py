from app.main import db


class Stock(db.Model):
    """
    Infos about the available stocks in the system
    """
    __tablename__ = 'stock'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Unicode, nullable=False, default="''")
    ticker = db.Column(db.Unicode, nullable=False, default="''")
    segment = db.Column(db.Unicode, nullable=False, default="''")
    image = db.Column(db.Unicode, nullable=False, default="''")

    def __repr__(self):
        return '<stock({}): name: {}, ticker: {}'.format(self.id, self.name, self.ticker)
