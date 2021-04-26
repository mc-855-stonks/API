from flask_restx import Namespace, fields

class HealthcheckDto:
    api = Namespace('healthcheck', description='endpoint for application healthcheck')
