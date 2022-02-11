from csv_cti.models.codes import Codes
from csv_cti.models import db
from csv_cti.blueprints.op.aes_models import AES_ENCRYPT
from flask import current_app
#短码拨号

class Codes_op():
    @staticmethod
    def add(codes_list):#Tiers信息map组成列表
        add_list=[]
        for i in codes_list:
            a=AES_ENCRYPT(current_app.config['AES_KEY'],current_app.config['AES_IV'])
            customer_number=a.decrypt(i['encrypted_number']).decode('UTF-8')
            add_list.append(Codes(group=i['group'],short_code=i['short_code'],customer_number=customer_number))
        with Codes.auto_commit(db):
            db.session.add_all(add_list)

    @staticmethod
    def remove(codes_list):#Tiers组成的map 列表     
        for i in codes_list:
            with Codes.auto_commit(db):
                a=Codes.query.filter(Codes.short_code==i['short_code']).first()
                if a:
                    db.session.delete(a)
       
    @staticmethod
    def query(codes_info):#只查询group为条件
        query_result_list=[]
        if codes_info.get('group'):
            with Codes.auto_commit(db):
                query_result=Codes.query.filter(Codes.group==codes_info['group']).order_by(Codes.id.desc()).paginate(codes_info['page_index'], per_page=codes_info['page_size'], error_out = False)
            for i in query_result.items:
                query_result_list.append(i.to_json())
            query_result_list.append(query_result.total)
            return query_result_list
        else:
            if codes_info.get('csv'):
                with Codes.auto_commit(db):
                    query_result=Codes.query.filter().all()
                for i in query_result:
                    query_result_list.append(i.to_json())
                return query_result_list
            else:
                with Codes.auto_commit(db):
                    query_result=Codes.query.filter().order_by(Codes.id.desc()).paginate(codes_info['page_index'], per_page=codes_info['page_size'], error_out = False)
                for i in query_result.items:
                    query_result_list.append(i.to_json())
                query_result_list.append(query_result.total)
                return query_result_list