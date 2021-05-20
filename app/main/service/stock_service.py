from app.main import db
from app.main.model.stock import Stock

def get_available_stocks():
    stocks = db.session.query(Stock).all()
    return stocks
