from csv_cti.models.queues import Queues
from csv_cti.models import db
from flask import current_app
from csv_cti.blueprints.op.csv_esl import Send_commands
from threading import Thread


class Queues_op():
    '''
    id                                              = db.Column(db.Integer,primary_key=True)
    name                                            = db.Column(db.String(10))
    group                                           = db.Column(db.String(10))
    strategy                                        = db.Column(db.String(255),default='longest-idle-agent')
    moh_sound                                       = db.Column(db.String(255),default='$${hold_music}')
    record_template                                 = db.Column(db.String(255),default='$${recordings_dir}/${strftime(%Y-%m-%d-%H-%M-%S)}.${destination_number}.${caller_id_number}.${uuid}.wav')
    time_base_score                                 = db.Column(db.String(10),default='system')#时基分数 queue or system
    max_wait_time                                   = db.Column(db.Integer,default=0)
    max_wait_time_with_no_agent                     = db.Column(db.Integer,default=0)
    max_wait_time_with_no_agent_time_reached        = db.Column(db.Integer,default=5)
    tier_rules_apply                                = db.Column(db.String(10),default='false')
    tier_rule_wait_second                           = db.Column(db.Integer,default=300)
    tier_rule_wait_multiply_level                   = db.Column(db.String(10),default='true')
    tier_rule_no_agent_no_wait                      = db.Column(db.String(10),default='false')
    discard_abandoned_after                         = db.Column(db.Integer,default=60)
    abandoned_resume_allowed                        = db.Column(db.String(10),default='false')
    '''

    @staticmethod
    def add(queues_list):#Queue信息map组成列表
        add_list=[]
        for i in queues_list:
            add_list.append(Queues(name=i['name'].lower(),group=i['group'].upper()))
        with Queues.auto_commit(db):
            db.session.add_all(add_list)
        for i in queues_list:
            t=Thread(target=Queues_op.send_command,args=['queue reload',current_app.config['ESL_DOMAIN'],current_app.config['ESL_PORT'],current_app.config['ESL_PASSWD'],i['name'].lower(),i['group'].lower()])
            t.start()
            #Queues_op.send_command('queue reload',current_app.config['ESL_DOMAIN'],current_app.config['ESL_PORT'],current_app.config['ESL_PASSWD'],i['name'].lower(),i['group'].lower())
        

    @staticmethod
    def remove(queues_list):#Queue组成的map 列表     
        for i in queues_list:
            with Queues.auto_commit(db):
                a=Queues.query.filter(Queues.name==i['name'].lower(),Queues.group==i['group'].upper()).first()
                if a:
                    db.session.delete(a)
            t=Thread(target=Queues_op.send_command,args=['queue reload',current_app.config['ESL_DOMAIN'],current_app.config['ESL_PORT'],current_app.config['ESL_PASSWD'],i['name'].lower(),i['group'].lower()])
            t.start()
       
    @staticmethod
    def query(queue_info):#分机号,doamin,group,extname组成的map
        query_result_list=[]
        if queue_info.get('group'):
            if queue_info.get('name'):
                with Queues.auto_commit(db):
                    query_result=Queues.query.filter(Queues.name==queue_info['name'].lower(),Queues.group==queue_info['group'].upper()).order_by(Queues.id.desc()).paginate(queue_info['page_index'], per_page=queue_info['page_size'], error_out = False)
                for i in query_result.items:
                    query_result_list.append(i.to_json())
                query_result_list.append(query_result.total)
                return query_result_list
            else:
                with Queues.auto_commit(db):
                    query_result=Queues.query.filter(Queues.group==queue_info['group'].upper()).order_by(Queues.id.desc()).paginate(queue_info['page_index'], per_page=queue_info['page_size'], error_out = False)
                for i in query_result.items:
                    query_result_list.append(i.to_json())
                query_result_list.append(query_result.total)
                return query_result_list           
        else:
            if queue_info.get('csv'):
                with Queues.auto_commit(db):
                    query_result=Queues.query.filter().all()
                for i in query_result:
                    query_result_list.append(i.to_json())
                return query_result_list
            else:
                with Queues.auto_commit(db):
                    query_result=Queues.query.filter().order_by(Queues.id.desc()).paginate(queue_info['page_index'], per_page=queue_info['page_size'], error_out = False)
                for i in query_result.items:
                    query_result_list.append(i.to_json())
                query_result_list.append(query_result.total)
                return query_result_list

    def send_command(cmd_type,host,port,passwd,name,group):
        new_send_commands=Send_commands(cmd_type,host,port,passwd,name=name,group=group)
        new_send_commands.send_call()