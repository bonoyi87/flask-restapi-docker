from wanted.extensions import db


class Service:

    __model__ = None

    def _isinstance(self, model, raise_error=True):
        if not isinstance(model, self.__model__) and raise_error:
            raise ValueError('%s is not of type %s' % (model, self.__model__))

    def all(self):
        return self.__model__.query.all()

    def get(self, id):
        return self.__model__.query.get(id)

    def get_all(self, *ids):
        if not ids:
            return []

        return self.__model__.query.filter(self.__model__.id.in_(ids)).all()

    def save(self, model):
        self._isinstance(model)
        self.session.add(model)
        self.session.flush()
        return model

    def create(self, **kwargs):
        return self.save(self.new(**kwargs))

    def update(self, model, **kwargs):
        self._isinstance(model)

        for k, v in kwargs.items():
            setattr(model, k, v)

        self.save(model)
        return model

    def delete(self, model):
        self._isinstance(model)

        self.session.delete(model)
        self.session.flush()

    def new(self, **kwargs):
        return self.__model__(**kwargs)

    @property
    def session(self):
        return db.session
