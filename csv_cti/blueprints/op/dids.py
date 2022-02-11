'''
    id    = db.Column(db.Integer,primary_key=True)
    did   = db.Column(db.String(30))
    queue = db.Column(db.String(30))
    group = db.Column(db.String(10))
'''
from csv_cti.models.dids import Dids
from csv_cti.models import db

class Dids_op():
    @staticmethod
    def add(dids_list):#Tiers信息map组成列表
        add_list=[]
        for i in dids_list:
            add_list.append(Dids(queue=i['queue'].lower(),did=i['did'],group=i['group'].upper()))
        with Dids.auto_commit(db):
            db.session.add_all(add_list)

    @staticmethod
    def remove(dids_list):#Tiers组成的map 列表     
        for i in dids_list:
            with Dids.auto_commit(db):
                a=Dids.query.filter(Dids.did==i['did']).first()
                if a:
                    db.session.delete(a)
       
    @staticmethod
    def query(dids_info):#只查询group为条件
        query_result_list=[]
        if dids_info.get('group'):
            with Dids.auto_commit(db):
                query_result=Dids.query.filter(Dids.group==dids_info['group'].upper()).order_by(Dids.id.desc()).paginate(dids_info['page_index'], per_page=dids_info['page_size'], error_out = False)
            for i in query_result.items:
                query_result_list.append(i.to_json())
            query_result_list.append(query_result.total)
            return query_result_list
        else:
            if dids_info.get('csv'):
                with Dids.auto_commit(db):
                    query_result=Dids.query.filter().all()
                for i in query_result:
                    query_result_list.append(i.to_json())
                return query_result_list
            else:
                with Dids.auto_commit(db):
                    query_result=Dids.query.filter().order_by(Dids.id.desc()).paginate(dids_info['page_index'], per_page=dids_info['page_size'], error_out = False)
                for i in query_result.items:
                    query_result_list.append(i.to_json())
                query_result_list.append(query_result.total)
                return query_result_list
        