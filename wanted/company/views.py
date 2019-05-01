from flask import Blueprint
from flask_restful import Api

from wanted.company.resources.tag import CompanyTagListResource

blueprint = Blueprint('api', __name__, url_prefix='/v1')
api = Api(blueprint)

api.add_resource(CompanyTagListResource, '/companies/<int:company_id>/tags')
