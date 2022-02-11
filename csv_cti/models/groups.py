from curses import keyname
from csv_cti.models import db
from contextlib import contextmanager

class Groups(db.Model):
    __tablename__ = 'groups'
    id    =    db.Column(db.Integer,primary_key=True)
    group = db.Column(db.String(10))
    token = db.Column(db.String(18))
    key   = db.Column(db.String(18))
    iv    = db.Column(db.String(18))
    mark = db.Column(db.String(30))

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
            'id':self.id,
            'group':self.group,
            'mark':self.mark,
            'token':self.token,
            'key':self.key,
            'iv':self.iv
        }