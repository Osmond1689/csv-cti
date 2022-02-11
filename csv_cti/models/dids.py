from . import db
from contextlib import contextmanager

class Dids(db.Model):
    __tablename__='dids'

    id    = db.Column(db.Integer,primary_key=True)
    did   = db.Column(db.String(30),unique=True)
    queue = db.Column(db.String(30))
    group = db.Column(db.String(10))

    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()  # 事务
        except Exception as e:
            self.session.rollback()  # 回滚
            raise e
    def to_json(self):
        return {
            'id': self.id,
            'did': self.did,
            'queue':self.queue,
            'group':self.group
        }