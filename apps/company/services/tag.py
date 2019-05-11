from apps.company.models import Tag
from apps.company.services import Service


class TagService(Service):

    __model__ = Tag


service = TagService()
