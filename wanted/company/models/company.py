import datetime as dt

from wanted.extensions import db


class Company(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.TIMESTAMP, default=dt.datetime.utcnow, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, onupdate=dt.datetime.utcnow)


class CompanyName(db.Model):
    __tablename__ = 'company_names'
    __table_args__ = (
        db.UniqueConstraint('company_id', 'lang'),
    )

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    lang = db.Column(db.String(2), nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=dt.datetime.utcnow, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, onupdate=dt.datetime.utcnow)


class Tag(db.Model):
    __tablename__ = 'tags'
    __table_args__ = (
        db.UniqueConstraint('tag'),
    )

    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(80), nullable=False)
    lang = db.Column(db.String(2), nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=dt.datetime.utcnow, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, onupdate=dt.datetime.utcnow)


class CompanyTag(db.Model):
    __tablename__ = 'company_tags'
    __table_args__ = (
        db.UniqueConstraint('company_id', 'tag_id'),
    )

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=dt.datetime.utcnow, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, onupdate=dt.datetime.utcnow)


class SearchCompany(db.Model):
    __tablename__ = 'search_companies'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    initial_index = db.Column(db.String(255), nullable=False)
    phoneme_index = db.Column(db.String(255), nullable=False)

    created_at = db.Column(db.TIMESTAMP, default=dt.datetime.utcnow, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, onupdate=dt.datetime.utcnow)
