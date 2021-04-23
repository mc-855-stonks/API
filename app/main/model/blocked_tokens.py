import datetime

from app.main import db


class BlockedToken(db.Model):
    """
    Token Model for storing blocked JWT tokens
    """
    __tablename__ = 'blocked_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blocked_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blocked_on = datetime.datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @staticmethod
    def check_blocked(auth_token):
        # check whether auth token has been blocked
        return bool(BlockedToken.query.filter_by(token=str(auth_token)).first())