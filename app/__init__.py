from flask_restx import Api
from flask import Blueprint

from app.main.controller import user_controller, auth_controller, stock_info_controller, healthcheck_controller

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='STONKS API',
          version='1.0',
          description='api for Stonks application'
          )

api.add_namespace(stock_info_controller.api)
api.add_namespace(auth_controller.api)
api.add_namespace(user_controller.api, path='/user')
api.add_namespace(healthcheck_controller.api, path="/healthcheck")