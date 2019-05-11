from http import HTTPStatus

from flask import request
from flask_restful import Resource, abort

from apps.company.models import CompanyTag, Company
from apps.company.models.company import Tag
from apps.company.services.tag import service as tag_service
from apps.company.services.company_tag import service as company_tag_service


class CompanyTagListResource(Resource):
    def post(self, company_id):
        request_data = request.get_json()
        if not Company.query.filter_by(id=company_id).count():
            abort(HTTPStatus.NOT_FOUND.value, message='Not Found company({})'.format(company_id))

        tag_name = request_data.get('name')
        tag_lang = request_data.get('lang')

        if CompanyTag.query.join(Tag).filter(Company.id == company_id, Tag.tag == tag_name).count():
            abort(HTTPStatus.CONFLICT.value, message='Already registered tag({})'.format(tag_name))

        tag = Tag.query.filter_by(tag=tag_name).first()
        if not tag:
            tag = tag_service.save(Tag(tag=tag_name, lang=tag_lang))

        company_tag_service.save(CompanyTag(company_id=company_id, tag_id=tag.id))

        return {}, HTTPStatus.CREATED.value


class CompanyTagResource(Resource):

    def delete(self, company_id, tag_id):
        if not CompanyTag.query.filter_by(company_id=company_id, tag_id=tag_id).count():
            abort(HTTPStatus.NOT_FOUND.value, message='Not Found company\'s tag')

        company_tag_service.delete_company_tag(company_id, tag_id)

        return {}, HTTPStatus.OK.value

