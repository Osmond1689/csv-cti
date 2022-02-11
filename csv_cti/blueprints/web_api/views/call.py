from flask import request
from csv_cti.blueprints.web_api import web_api
#from werkzeug.local import Local
from csv_cti.blueprints.op.csv_esl import Send_commands
import _thread
from csv_cti.blueprints.op.md5_token import encrypt_md5
from csv_cti.blueprints.op.aes_models import AES_ENCRYPT
from flask import current_app
from csv_cti.blueprints.op.redis import redis_client
from csv_cti.blueprints.op.agents import Agents_op


def send_command(cmd_type,host,port,passwd,crm_uuid=None,extensin_number=None,customer_number=None,agent=None,product_code=None):
    new_send_commands=Send_commands(cmd_type,host,port,passwd,crm_uuid,extensin_number,customer_number,agent,product_code)
    new_send_commands.send_call()
    # return_data['data']=new_send_commands.job_status



@web_api.route('/click-on-call/',methods=['POST'])
def click_on_call():
    '''
    {
			"token":"97d5fc0bdfc499fc8a008199cab1be53",
			"data":{
                "crm_uuid":xxx,必选
                "extensin_number":xxx必选
                "customer_number":xxx必选aes_cbc128加密
                "product_code":xxx必选,
                "agent":xxx,
            }
	}
    '''
    return_data={}
    r_token=request.json.get('token')
    if r_token in encrypt_md5(current_app.config['MD5_KEY']):
        r_json=request.json.get('data')
        login_data={"group":r_json.get('group'),"name":r_json.get('agent'),"page_index":1,"page_size":10}
        try:
            list=Agents_op.query(login_data)
        except Exception as e:
            current_app.logger.debug("/click-on-call/ 数据库操作失败：%s",e)
            return_data['msg']='Voice abnormal, Please contact the Voice engineer'
            return return_data,500
        else:
            if not list[0]:
                current_app.logger.info("/click-on-call/ %s 呼叫失败，座席号不存在",r_json.get('agent'))
                return_data['msg']='Agent Does Not Exist'
                return return_data,404
            else:
                real_agent_passwd=list[0].get('password')
        if r_json.get('agent_password')==real_agent_passwd:
            if redis_client.exists(r_json.get('extensin_number')+'_ext'):
                agent=redis_client.lrange(r_json.get('extensin_number')+'_ext',0,-1)[1].decode('utf-8')
                if agent==r_json.get('agent'):
                    crm_uuid=r_json.get('crm_uuid')
                    extensin_number=r_json.get('extensin_number')
                    call_func=r_json.get('call_func')
                    customer_number_encrypt=r_json.get('customer_number')
                    if customer_number_encrypt:
                        a=AES_ENCRYPT(current_app.config['AES_KEY'],current_app.config['AES_IV'])
                        customer_number=(a.decrypt(customer_number_encrypt)).decode('UTF-8')
                    product_code=r_json.get('product_code')
                    #call_type=r_json.get('call_type')
                    #if 1:5t  
                    if crm_uuid and extensin_number and customer_number and product_code:
                        if call_func:
                            #异步调用ESL
                            try:
                                _thread.start_new_thread(send_command,('click_on_call_dtmf',current_app.config['ESL_DOMAIN'],current_app.config['ESL_PORT'],current_app.config['ESL_PASSWD'],crm_uuid,extensin_number,customer_number,agent,product_code))
                            except Exception as e:
                                current_app.logger.debug("/click-on-call/ 连接ESL失败：%s",e)
                                return_data['msg']='Voice abnormal, Please contact the Voice engineer'
                                return return_data,500
                            else:
                                current_app.logger.info("/click-on-call/ 接口调用成功:crm_uuid：%s，extensin_number：%s，customer_number： %s,agent %s,product_code：%s,绑定dtmf",crm_uuid,extensin_number,customer_number,agent,product_code)
                                return_data['msg']='Call OK'
                                return return_data,200
                        else:
                            #异步调用ESL
                            try:
                                _thread.start_new_thread(send_command,('click_on_call',current_app.config['ESL_DOMAIN'],current_app.config['ESL_PORT'],current_app.config['ESL_PASSWD'],crm_uuid,extensin_number,customer_number,agent,product_code))
                            except Exception as e:
                                current_app.logger.debug("/click-on-call/ 连接ESL失败：%s",e)
                                return_data['msg']='Voice abnormal, Please contact the Voice engineer'
                                return return_data,500
                            else:
                                current_app.logger.info("/click-on-call/ 接口调用成功:crm_uuid：%s，extensin_number：%s，customer_number： %s,agent %s,product_code：%s",crm_uuid,extensin_number,customer_number,agent,product_code)
                                return_data['msg']='Call OK'
                                return return_data,200
                    else:
                        return_data['msg']='The parameter is wrong'
                        return return_data,502
                else:
                        return_data['msg']='The binding relationship is error'
                        return return_data,402
            else:
                return_data['msg']='Unbound Agent'
                return return_data,403
        else:
            return_data['msg']='Agent Password Error'
            return return_data,402
    else:
        return_data['msg']='Auth Fail'
        return return_data,401
    





