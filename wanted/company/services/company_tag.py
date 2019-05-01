from wanted.company.models import CompanyTag
from wanted.company.services import Service


class CompanyTagService(Service):

    __model__ = CompanyTag

    def delete_company_tag(self, company_id: int, tag_id: int):
        """

        :param company_id:
        :param tag_id:
        :return:
        """

        company_tag = self.__model__.query.filter_by(company_id=company_id, tag_id=tag_id).first()

        if company_tag:
            self.delete(company_tag)


service = CompanyTagService()
