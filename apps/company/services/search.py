from utils.word import get_hangul, has_chosung, seperate_word
from apps.company.models import SearchCompany, Company
from apps.company.services import Service


class SearchCompanyService(Service):

    __model__ = SearchCompany

    def search(self, q: str):
        """
        회사명 검색
        :param q:
        :return:
        """

        only_hangul = get_hangul(q)
        base_query = SearchCompany.query.join(Company).with_entities(Company).distinct()

        if has_chosung(only_hangul):
            # q 가 초성만 있다면 initial_index 에서 검색
            base_query = base_query.filter(SearchCompany.initial_index.like('%{}%'.format(q)))
        else:
            base_query = base_query.filter(SearchCompany.phoneme_index.like('%{}%'.format(seperate_word(q))))

        return base_query.all()


service = SearchCompanyService()
