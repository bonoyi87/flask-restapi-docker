import re
from enum import Enum

from flask_restful import Resource, fields, marshal_with
from flask import request

from utils.word import seperate_word
from wanted.company.models import SearchCompany, Company, CompanyTag
from wanted.company.models.company import Tag


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

            regex_only_hangul = re.compile('[ㄱ-ㅎㅏ-ㅣ가-힣]')
            only_hangul = "".join(regex_only_hangul.findall(q))
            regex = re.compile(r"[ㄱ-ㅎ]")
            has_chosung = regex.match(only_hangul)

            base_query = SearchCompany.query.join(Company).with_entities(Company).distinct()

            if has_chosung:
                base_query = base_query.filter(SearchCompany.initial_index.like('%{}%'.format(q)))
            else:
                base_query = base_query.filter(SearchCompany.phoneme_index.like('%{}%'.format(seperate_word(q))))

            return base_query.all()

        elif search_type == SearchType.TAG.value:
            base_query = CompanyTag.query.join(Tag).filter(Tag.tag == q).with_entities(Company)
            return base_query.all()

        return {}, 400
