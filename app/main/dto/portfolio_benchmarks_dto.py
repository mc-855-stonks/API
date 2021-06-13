from flask_restx import Namespace, fields


class PortfolioBenchmarksDto:
    api = Namespace('benchmarks', description='Get portfolio returns and benchmarks')
