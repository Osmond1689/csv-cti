'''
    id    =    db.Colmun(db.Integer,primary_key=True)
    group = db.Colmun(db.String(30))
    mark = db.Colmun(db.String(255))
'''
from lib2to3.pgen2 import token
from csv_cti.models.groups import Groups
from csv_cti.models import db

class Groups_op():
    @staticmethod
    def add(groups_list):#Tiers信息map组成列表
        add_list=[]
        for i in groups_list:
            add_list.append(Groups(group=i['group'].upper(),token=i['token'],aes=i['aes'],iv=i['iv'],mark=i['mark']))
        with Groups.auto_commit(db):
            db.session.add_all(add_list)

    @staticmethod
    def remove(groups_list):#Tiers组成的map 列表     
        for i in groups_list:
            with Groups.auto_commit(db):
                a=Groups.query.filter(Groups.group==i['group'].upper()).first()
                if a:
                    db.session.delete(a)
       
    @staticmethod
    def query(groups_info):#只查询group为条件
        query_result_list=[]
        if groups_info.get('group'):
            with Groups.auto_commit(db):
                query_result=Groups.query.filter(Groups.group==groups_info['group'].upper()).order_by(Groups.id.desc()).paginate(groups_info['page_index'], per_page=groups_info['page_size'], error_out = False)
            for i in query_result.items:
                query_result_list.append(i.to_json())
            query_result_list.append(query_result.total)
            return query_result_list
        else:
            with Groups.auto_commit(db):
                query_result=Groups.query.filter().order_by(Groups.id.desc()).paginate(groups_info['page_index'], per_page=groups_info['page_size'], error_out = False)
            for i in query_result.items:
                query_result_list.append(i.to_json())
            query_result_list.append(query_result.total)
            return query_result_list
    @staticmethod
    def auth(groups_info):#只查询group为条件
        pass