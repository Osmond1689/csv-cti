from . import db
from contextlib import contextmanager

class Exts(db.Model):
    __tablename__="exts"

    id = db.Column(db.Integer,primary_key=True)
    extnumber= db.Column(db.String(10))
    extname= db.Column(db.String(10))
    group= db.Column(db.String(30))
    password= db.Column(db.String(30))
    
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
            'extnumber': self.extnumber,
            'extname': self.extname,
            'password':self.password,
            'group':self.group
        }
    
