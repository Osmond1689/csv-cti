from csv_cti.models.exts import Exts
from csv_cti.models import db
from flask import current_app


class Exts_op():
    
    '''
    ext={
            'group':'default',
            'extnumber':sip_auth_username,
            'password':'123456',
            'extname':'osmond'
        }
    '''
    @staticmethod
    def add(ext_info_list):#分机信息map组成列表
        add_list=[]
        for i in ext_info_list:
            if not i.get('extname'):
                i['extname']=i['extnumber']
            add_list.append(Exts(group=i['group'].upper(),extnumber=i['extnumber'],password=i['password'],extname=i['extname'].lower()))
            current_app.logger.info("分机添加接口调用成功:%s:%s",i['extname'].lower(),i['extnumber'])
        with Exts.auto_commit(db):
            db.session.add_all(add_list)

    @staticmethod
    def remove(ext_info_list):#分机号,doamin组成的map 列表
        with Exts.auto_commit(db):
            for i in ext_info_list:
                a=Exts.query.filter(Exts.group==i['group'].upper(),Exts.extnumber==i['extnumber']).first()
                if a:
                    db.session.delete(a)

        
    @staticmethod
    def change(ext_info_list):#分机号,doamin组成的map 列表
        with Exts.auto_commit(db):
            for i in ext_info_list:
                #所有参数必传
                Exts.query.filter(Exts.extnumber==i['extnumber']).update({'group':i['group'].upper(),'password':i['password'],'extname':i['extname'].lower()})
                
    @staticmethod
    def query(ext_info):#group,extname组成的map三种查询结果  group extnumber 全部
        query_result_list=[]
        if ext_info.get('group'):
            if ext_info.get('extnumber') :
                if ext_info.get('auth')=='Y':
                    query_result=Exts.query.filter(Exts.extnumber==ext_info['extnumber']).first()
                    return query_result.to_json()
                else:
                    query_result=Exts.query.filter(Exts.extnumber==ext_info['extnumber']).order_by(Exts.id.desc()).paginate(ext_info['page_index'], per_page=ext_info['page_size'], error_out = False)
                    for i in query_result.items:
                        query_result_list.append(i.to_json())
                    query_result_list.append(query_result.total)
                    return query_result_list
            else:
                query_result=Exts.query.filter(Exts.group==ext_info['group'].upper()).order_by(Exts.id.desc()).paginate(ext_info['page_index'], per_page=ext_info['page_size'], error_out = False)
                for i in query_result.items:
                    query_result_list.append(i.to_json())
                query_result_list.append(query_result.total)
                return query_result_list
        else:
            query_result=Exts.query.filter().order_by(Exts.id.desc()).paginate(ext_info['page_index'], per_page=ext_info['page_size'], error_out = False)
            for i in query_result.items:
                query_result_list.append(i.to_json())
            query_result_list.append(query_result.total)
            return query_result_list
