from app.main import db
from app.main.model.stock import Stock


def get_available_stocks():
    stocks = db.session.query(Stock).all()
    return [{
        'name': s.name,
        'ticker': s.ticker,
        'segment': s.segment,
        'image': s.image,
        'id': s.id
    } for s in stocks]
