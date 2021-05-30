from flask_restx import Api
from flask import Blueprint

from app.main.controller import operation_controller, user_controller, \
    auth_controller, stock_info_controller, healthcheck_controller, wallet_controller, stock_controller, \
    portfolio_controller, portfolio_performance_controller, stock_history_controller


blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='STONKS API',
          version='1.0',
          description='api for Stonks application'
          )

api.add_namespace(stock_info_controller.api)
api.add_namespace(auth_controller.api)
api.add_namespace(user_controller.api, path='/user')
api.add_namespace(operation_controller.api, path='/operation')
api.add_namespace(wallet_controller.api, path='/wallet')
api.add_namespace(portfolio_controller.api, path='/portfolio')
api.add_namespace(portfolio_performance_controller.api, path='/performance')
api.add_namespace(healthcheck_controller.api, path="/healthcheck")
api.add_namespace(stock_controller.api, path="/stock")
api.add_namespace(stock_history_controller.api, path="/stock_hist")

