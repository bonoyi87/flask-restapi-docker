from wanted.extensions import db
import datetime as dt


class CreatedAtMixin(db.Model):
    created_at = db.Column(db.TIMESTAMP, default=dt.datetime.utcnow, nullable=False)


class UpdatedAtMixin(db.Model):
    updated_at = db.Column(db.TIMESTAMP, onupdate=dt.datetime.utcnow)


class TimestampMixin(CreatedAtMixin, UpdatedAtMixin):
    pass
