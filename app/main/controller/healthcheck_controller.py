from flask_restx import Resource
from app.main.service.healthcheck_service import healthcheck
from app.main.dto.healthcheck_dto import HealthcheckDto

api = HealthcheckDto.api

@api.route('/')
class Healthcheck(Resource):
    @api.response(200, 'Healthcheck returns OK')
    @api.doc('Healthcheck endpoint.')
    def get(self):
        return healthcheck()
