from flask_restx import Namespace, fields


class PortfolioDto:
    api = Namespace('portfolio', description='Portfolio related operations')
