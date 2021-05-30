from flask_restx import Namespace, fields


class PortfolioPerformanceDto:
    api = Namespace('performance', description='Get portfolio performance metrics')
