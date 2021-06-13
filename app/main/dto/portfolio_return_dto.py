from flask_restx import Namespace, fields


class PortfolioReturnDto:
    api = Namespace('return', description='Get portfolio return')
