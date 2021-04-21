from flask_restx import Api
from flask import Blueprint

from app.main.controller import user_controller

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='STONKS API',
          version='1.0',
          description='api for Stonks application'
          )

api.add_namespace(user_controller.api, path='/user')