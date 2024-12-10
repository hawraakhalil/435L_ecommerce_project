from sqlalchemy.ext.declarative import declared_attr
from shared.db import db
from shared.utils.utils import get_utc_now

class BaseModel(object):
    __abstract__ = True

    @declared_attr
    def created_at(cls):
        return db.Column(db.DateTime, default=get_utc_now, nullable=False)

    @declared_attr
    def updated_at(cls):
        return db.Column(db.DateTime, default=get_utc_now, onupdate=get_utc_now, nullable=False)
