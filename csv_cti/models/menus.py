from enum import unique
from . import db
from contextlib import contextmanager

class Menus(db.Model):
    __tablename__="menus"

    id = db.Column(db.Integer,primary_key=True)
    name= db.Column(db.String(20),unique=True)
    key1= db.Column(db.String(20),unique=True)
    key2= db.Column(db.String(20),unique=True)
    type= db.Column(db.Intger) #1菜单 2 按钮 3栏位
    sort = db.Column(db.Intger)

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

class Menu_relation(db.Model):
    __tablename__="menu_relation"

    id = db.Column(db.Integer,primary_key=True)
    child = db.Column(db.String(20))
    parent = db.Column(db.String(20))
    deepth = db.Column(db.Intger)

    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()  # 事务
        except Exception as e:
            self.session.rollback()  # 回滚
            raise e
    def to_json(self):
        di={}
        for c in self.__class__.__table__.columns:
            v = getattr(self, c.name)
            di[c.name] = v
        return di

