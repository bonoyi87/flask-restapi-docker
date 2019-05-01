from enum import Enum
from http import HTTPStatus
from flask_restful import Resource, fields, marshal_with, abort
from flask import request

from wanted.company.models import Company, CompanyTag, Tag
from wanted.company.services.search import service as search_service


class SearchType(Enum):
    COMPANY = 'company'
    TAG = 'tag'


tag_fields = {'id': fields.Integer(attribute='tag.id'),
              'tag': fields.String(attribute='tag.tag'),
              'lang': fields.String(attribute='tag.lang')}

name_fields = {'name': fields.String,
               'lang': fields.String}

company_fields = {
    'id': fields.Integer,
    'names': fields.List(fields.Nested(name_fields)),
    'tags': fields.List(fields.Nested(tag_fields))
}


class SearchCompanyResource(Resource):
    @marshal_with(company_fields, envelope='companies')
    def get(self):
        q = request.args.get('q')
        search_type = request.args.get('type', SearchType.COMPANY.value)  # 검색타입
        if search_type == SearchType.COMPANY.value:

            return search_service.search(q)

        elif search_type == SearchType.TAG.value:
            base_query = CompanyTag.query.join(Tag).filter(Tag.tag == q).with_entities(Company)
            return base_query.all()

        abort(HTTPStatus.BAD_REQUEST.value, message="Invalid Search Type")
