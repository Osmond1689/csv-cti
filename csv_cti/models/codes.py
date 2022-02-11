from . import db
from contextlib import contextmanager

class Codes(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    short_code=db.Column(db.String(8),unique=True)
    customer_number=db.Column(db.String(50))

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
            'short_code': self.short_code,
            'customer_number':self.customer_number
        }
