from wanted.company.models import Tag
from wanted.company.services import Service


class TagService(Service):

    __model__ = Tag


service = TagService()
