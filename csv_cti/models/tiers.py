from . import db
from contextlib import contextmanager
'''
 queue    | character varying(255) |           |          | 
 agent    | character varying(255) |           |          | 
 state    | character varying(255) |           |          | 
 level    | integer                |           | not null | 1
 position | integer                |           | not null | 1
'''
class Tiers(db.Model):
    __tablename__ = 'tiers'
    id       =db.Column(db.Integer,primary_key=True)
    queue    =db.Column(db.String(255))
    agent    =db.Column(db.String(255))
    state    =db.Column(db.String(255),default='Ready')
    group    =db.Column(db.String(255))
    level    =db.Column(db.Integer,nullable=False,default=1)
    position =db.Column(db.Integer,nullable=False,default=1)

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
            'id'       : self.id,  
            'group'    : self.group,
            'agent'    : self.agent,
            'state'    : self.state,
            'level'    : self.level,
            'position' : self.position
        }
