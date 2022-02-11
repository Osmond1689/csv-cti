from csv_cti.models.agents import Agents
from csv_cti.models import db
from flask import current_app
from csv_cti.blueprints.op.md5_token import encrypt_agent_md5

class Agents_op():
    '''
    name                 =db.Column(db.String(255))  #1001@default
    instance_id          =db.Column(db.String(255))  #single_box
    uuid                 =db.Column(db.String(255))  #uuid
    type                 =db.Column(db.String(255))  #callback
    contact              =db.Column(db.String(1024)) #user/1001
    status               =db.Column(db.String(255))  #Logged out,Available
    state                =db.Column(db.String(255))  #Waiting
    '''

    @staticmethod
    def add(agents_list):#agents信息map组成列表
        add_list=[]
        for i in agents_list:
        #需要加正则校验contact 暂时无
            if i.get('contact'):
                add_list.append(Agents(name=i['name'].lower(),group=i['group'].upper(),password=encrypt_agent_md5(i['agent_password']),contact='[leg_timeout=10]user/'+i['contact']))
            else:
                add_list.append(Agents(name=i['name'].lower(),group=i['group'].upper(),password=encrypt_agent_md5(i['agent_password']),contact='[leg_timeout=10]user/000000'))
        with Agents.auto_commit(db):
            db.session.add_all(add_list)
            
    @staticmethod
    def remove(agents_list):#agents组成的map 列表     
        for i in agents_list:
            with Agents.auto_commit(db):
                a=Agents.query.filter(Agents.name==i['name'].lower(),Agents.group==i['group'].upper()).first()
                if a:
                    db.session.delete(a)
       
    @staticmethod
    def query(agents_info):#分机号,doamin,group,extname组成的map
        query_result_list=[] 
        if agents_info.get('group'):
            if agents_info.get('name'):
                with Agents.auto_commit(db):
                    query_result=Agents.query.filter(Agents.name==agents_info['name'].lower(),Agents.group==agents_info['group'].upper()).order_by(Agents.id.desc()).paginate(agents_info['page_index'], per_page=agents_info['page_size'], error_out = False)
                for i in query_result.items:
                    query_result_list.append(i.to_json())
                query_result_list.append(query_result.total)
                return query_result_list
            else:
                with Agents.auto_commit(db):
                    query_result=Agents.query.filter(Agents.group==agents_info['group'].upper).order_by(Agents.id.desc()).paginate(agents_info['page_index'], per_page=agents_info['page_size'], error_out = False)
                for i in query_result.items:
                    query_result_list.append(i.to_json())
                query_result_list.append(query_result.total)
                return query_result_list
        else:
            with Agents.auto_commit(db):
                query_result=Agents.query.filter().order_by(Agents.id.desc()).paginate(agents_info['page_index'], per_page=agents_info['page_size'], error_out = False)
            for i in query_result.items:
                    query_result_list.append(i.to_json())
            query_result_list.append(query_result.total)
            return query_result_list
    @staticmethod       
    def login(Agents_info):#分机号,doamin组成的map 列表
        with Agents.auto_commit(db):
            Agents.query.filter(Agents.name==Agents_info['agent'].lower(),Agents.group==Agents_info['group'].upper()).update({'contact':'[leg_timeout=10]user/'+Agents_info['ext'],'status':'Available'})

    @staticmethod       
    def logout(Agents_info):#分机号,doamin组成的map 列表
        with Agents.auto_commit(db):
            Agents.query.filter(Agents.name==Agents_info['agent'].lower(),Agents.group==Agents_info['group'].upper()).update({'status':'On Break'})        