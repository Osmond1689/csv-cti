from . import db
from contextlib import contextmanager

class Roles(db.Model):
    __tablename__="roles"

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20))
    menus = db.Column(db.String(255))
    
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()  # 事务
        except Exception as e:
            self.session.rollback()  # 回滚
            raise e
    def to_json(self):
        d={}
        for c in self.__class__.__table__.columns:
            v = getattr(self, c.name)
            d[c.name] = v
        return d