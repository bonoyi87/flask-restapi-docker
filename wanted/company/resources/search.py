from enum import Enum

from flask_restful import Resource, fields, marshal_with
from flask import request

from utils.word import seperate_word, get_hangul, has_chosung
from wanted.company.models import SearchCompany, Company, CompanyTag, Tag


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

            only_hangul = get_hangul(q)
            base_query = SearchCompany.query.join(Company).with_entities(Company).distinct()

            if has_chosung(only_hangul):
                # q 가 초성만 있다면 initial_index 에거 검색
                base_query = base_query.filter(SearchCompany.initial_index.like('%{}%'.format(q)))
            else:
                base_query = base_query.filter(SearchCompany.phoneme_index.like('%{}%'.format(seperate_word(q))))

            return base_query.all()

        elif search_type == SearchType.TAG.value:
            base_query = CompanyTag.query.join(Tag).filter(Tag.tag == q).with_entities(Company)
            return base_query.all()

        return {}, 400
