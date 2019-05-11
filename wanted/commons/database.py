from wanted.extensions import db
import datetime as dt


class CreatedAtMixin(db.Model):
    __abstract__ = True

    created_at = db.Column(db.TIMESTAMP, default=dt.datetime.utcnow, nullable=False)


class UpdatedAtMixin(db.Model):
    __abstract__ = True

    updated_at = db.Column(db.TIMESTAMP, onupdate=dt.datetime.utcnow)


class TimestampMixin(CreatedAtMixin, UpdatedAtMixin):
    __abstract__ = True
