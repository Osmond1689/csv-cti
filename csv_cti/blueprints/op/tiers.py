'''
 queue    | character varying(255) |           |          | 
 agent    | character varying(255) |           |          | 
 state    | character varying(255) |           |          | 
 level    | integer                |           | not null | 1
 position | integer                |           | not null | 1
'''
from csv_cti.models.tiers import Tiers
from csv_cti.models import db

class Tiers_op():
    @staticmethod
    def add(tiers_list):#Tiers信息map组成列表
        add_list=[]
        for i in tiers_list:
            if i.get('level'):
                if i.get('position'):
                #需要校验queue是否存在
                    add_list.append(Tiers(queue=i['queue'].lower()+'_'+i['group'].lower(),agent=i['agent'].lower(),level=i['level'],position=i['position'],group=i['group'].upper()))
                else:
                    add_list.append(Tiers(queue=i['queue'].lower()+'_'+i['group'].lower(),agent=i['agent'].lower(),level=i['level'],group=i['group'].upper()))
            elif i.get('position'):
                add_list.append(Tiers(queue=i['queue'].lower()+'_'+i['group'].lower(),agent=i['agent'].lower(),position=i['position'],group=i['group'].upper()))
            else:
                add_list.append(Tiers(queue=i['queue'].lower()+'_'+i['group'].lower(),agent=i['agent'].lower(),group=i['group'].upper()))
        with Tiers.auto_commit(db):
            db.session.add_all(add_list)

    @staticmethod
    def remove(tiers_list):#Tiers组成的map 列表     
        for i in tiers_list:
            with Tiers.auto_commit(db):
                a=Tiers.query.filter(Tiers.queue==i['queue'].lower()+'_'+i['group'].lower(),Tiers.agent==i['agent'].lower()).first()
                if a:
                    db.session.delete(a)
       
    @staticmethod
    def query(tiers_info):#只查询queue为条件
        query_result_list=[]
        with Tiers.auto_commit(db):
            query_result=Tiers.query.filter(Tiers.queue==tiers_info['queue'].lower()+'_'+tiers_info['group'].lower()).order_by(Tiers.id.desc()).paginate(tiers_info['page_index'], per_page=tiers_info['page_size'], error_out = False)
        for i in query_result.items:
            query_result_list.append(i.to_json())
        query_result_list.append(query_result.total)
        return query_result_list