from csv_cti.blueprints.web_api import web_api
from flask import request,current_app
from csv_cti.blueprints.op.md5_token import encrypt_md5
from csv_cti.blueprints.op.queues import Queues_op
from csv_cti.blueprints.op.csv_esl import Send_commands


def send_command(cmd_type,host,port,passwd,crm_uuid=None,extensin_number=None,customer_number=None,product_code=None):
    new_send_commands=Send_commands(cmd_type,host,port,passwd,crm_uuid,extensin_number,customer_number,product_code)
    new_send_commands.send_call()
    # return_data['data']=new_send_commands.job_status
#queue
@web_api.route('/queue-out-call/',methods=['POST'])
def queue_out_call():
    '''
    队列名称
    客户列表
    并发数量
    接听策略
    '''
    pass

@web_api.route('/queues-add/',methods=['POST'])
def queues_add():
    return_data={}
    r_token=request.json.get('token')
    if r_token in encrypt_md5(current_app.config['MD5_KEY']):
        r_data=request.json.get('data')
        '''
        {
			"token":"aecsv@88tech.net",
			"data":
            [{
            "name":"test",//必选
            "group":"C68"//必选
            
            }]
		}
        '''
        
        try:
            Queues_op.add(r_data)
        except Exception as e:
            current_app.logger.debug("/queues-add/ 数据库操作失败：%s",e)
            return_data['msg']='Voice abnormal, Please contact the Voice engineer'
            return return_data,500
        else:
            current_app.logger.info("/queues-add/ 添加成功")
            return_data['msg']='Add OK'
            return return_data,200
    else:
        return_data['msg']='Auth Fail'
        return return_data,401

@web_api.route('/queues-rm/',methods=['POST'])
def queues_rm():
    return_data={}
    r_token=request.json.get('token')
    if r_token in encrypt_md5(current_app.config['MD5_KEY']):
        r_data=request.json.get('data')
        '''
        {
			"token":"aecsv@88tech.net",
			"data"://留空查所有
            [{
            "name":"test",//必选
            "group":"C68"//必选
            }]
		}
        '''
        try:
            Queues_op.remove(r_data)
        except Exception as e:
            current_app.logger.debug("/queues-rm/ 数据库操作失败：%s",e)
            return_data['msg']='Voice abnormal, Please contact the Voice engineer'
            return return_data,500
        else:
            current_app.logger.info("/queues-rm/ 删除成功")
            return_data['msg']='Remove OK'
            return return_data,200
    else:
        return_data['msg']='Auth Fail'
        return return_data,401

@web_api.route('/queues-list/',methods=['POST'])
def queues_list():
    return_data={}
    r_token=request.json.get('token')
    if r_token in encrypt_md5(current_app.config['MD5_KEY']):
        r_data=request.json.get('data')
        '''
        {
			"token":"aecsv@88tech.net",
			"data"://留空字符串查所有
            {
                "name":"x",//可选
                "group":"C68"//可选
            }
		}
        '''
        try:
            list=Queues_op.query(r_data)
        except Exception as e:
            current_app.logger.debug("/queues-list/ 数据库操作失败：%s",e)
            return_data['msg']='Voice abnormal, Please contact the Voice engineer'
            return return_data,500
        else:
            current_app.logger.info("/queues-list/ 查询成功")
            return_data['msg']='Query OK'
            return_data['data']=list[0:-1]
            return_data['total']=list[-1]
            return return_data,200
    else:
        return_data['msg']='Auth Fail'
        return return_data,401

@web_api.route('/queues-reload/',methods=['POST'])
def queues_reload():
    '''
        {
			"token":"36ad10c7b8ded102658aeb4b241f48cc",
			"data":{}留空
		}
        '''
    return_data={}
    r_token=request.json.get('token')
    if r_token in encrypt_md5(current_app.config['MD5_KEY']):
        try:
            send_command('reload_mod_callcenter',current_app.config['ESL_DOMAIN'],current_app.config['ESL_PORT'],current_app.config['ESL_PASSWD'])
        except Exception as e:
            current_app.logger.debug("/queues-reload/ 连接ESL失败：%s",e)
            return_data['msg']='Voice abnormal, Please contact the Voice engineer'
            return return_data,500
        else:
            current_app.logger.info("/queues-reload/ 接口调用成功:reload_mod_callcenter")
            return_data['msg']='Call OK'
            return return_data,200
    else:
        return_data['msg']='Auth Fail'
        return return_data,401