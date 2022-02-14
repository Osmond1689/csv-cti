from . import db
from contextlib import contextmanager

class Users(db.Model):
    __tablename__="users"

    id = db.Column(db.Integer,primary_key=True)
    user= db.Column(db.String(10))
    password= db.Column(db.String(10))
    group= db.Column(db.String(30))
    agent= db.Column(db.String(30))
    role= db.Column(db.String(10))
    
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
            if c.name=="password":
                pass
            else:
                d[c.name] = v
        return d
    def to_auth_json(self):
        di={}
        for c in self.__class__.__table__.columns:
            v = getattr(self, c.name)
            di[c.name] = v
        return di
    
