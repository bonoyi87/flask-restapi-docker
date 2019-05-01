
from flask import request
from flask_restful import Resource

from wanted.company.models import CompanyTag, Company
from wanted.company.models.company import Tag
from wanted.extensions import db


class CompanyTagListResource(Resource):
    def post(self, company_id):
        request_data = request.get_json()
        if not Company.query.filter_by(id=company_id).count():
            return {}, 404
        tag_name = request_data.get('name')
        tag_lang = request_data.get('lang')

        if CompanyTag.query.join(Tag).filter(Company.id == company_id, Tag.tag == tag_name).count():
            return {}, 409

        tag = Tag.query.filter_by(tag=tag_name).first()
        if not tag:
            tag = Tag(tag=tag_name, lang=tag_lang)
            db.session.add(tag)
            db.session.commit()

        db.session.add(CompanyTag(company_id=company_id, tag_id=tag.id))
        db.session.commit()

        return {}, 201


class CompanyTagResource(Resource):

    def delete(self, company_id, tag_id):
        if not CompanyTag.query.filter_by(company_id=company_id, tag_id=tag_id).count():
            return {}, 404

        db.session.query(CompanyTag).filter_by(company_id=company_id, tag_id=tag_id).delete(synchronize_session=False)
        db.session.commit()
        return {}, 200

