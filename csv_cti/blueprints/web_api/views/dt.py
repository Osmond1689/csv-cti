from flask import request,current_app
from csv_cti.blueprints.web_api import web_api
from csv_cti.blueprints.op.md5_token import encrypt_md5

@web_api.route('/code-add/',methods=['POST'])
def code_add():
    return_data={}
    r_token=request.json.get('token')
    if r_token in encrypt_md5(current_app.config['MD5_KEY']):
        r_data=request.json.get('data')
        '''
        {
			"token":"aecsv@88tech.net",
			"data":[{
                "queue":"osmond2",//必选
                "agent":"50008",//必选
                "state":"Ready",//可选 default=Ready
                "level":1,//可选 default=1,
                "position":1,//可选 default=1
                "group":"C68"//必选
            }]
		}
        '''
        
        try:
            code_op.add(r_data)
        except Exception as e:
            current_app.logger.debug("/code-add/ 数据库操作失败：%s",e)
            return_data['msg']='Voice abnormal, Please contact the Voice engineer'
            return return_data,500
        else:
            current_app.logger.info("/code-add/ 添加成功")
            return_data['msg']='Add OK'
            return return_data,200
    else:
        return_data['msg']='Auth Fail'
        return return_data,401

@web_api.route('/code-rm/',methods=['POST'])
def code_rm():
    return_data={}
    r_token=request.json.get('token')
    if r_token in encrypt_md5(current_app.config['MD5_KEY']):
        r_data=request.json.get('data')
        '''
        {
			"token":"aecsv@88tech.net",
			"data":
            [{
                "agent":"50008",
                "queue":"osmond2",//必选
                "group":"C68"//必选
            }]
		}
        '''
        try:
            code_op.remove(r_data)
        except Exception as e:
            current_app.logger.debug("/code-rm/ 数据库操作失败：%s",e)
            return_data['msg']='Voice abnormal, Please contact the Voice engineer'
            return return_data,500
        else:
            current_app.logger.info("/code-rm/ 删除成功")
            return_data['msg']='Remove OK'
            return return_data,200
    else:
        return_data['msg']='Auth Fail'
        return return_data,401

@web_api.route('/code-list/',methods=['POST'])
def code_list():
    return_data={}
    r_token=request.json.get('token')
    if r_token in encrypt_md5(current_app.config['MD5_KEY']):
        r_data=request.json.get('data')
        '''
        {
			"token":"aecsv@88tech.net",
			"data":
            {
                "queue":"osmond2",//必选
                "group":"C68"//必选
            }
		}
        '''
        try:
            list=code_op.query(r_data)
        except Exception as e:
            current_app.logger.debug("/code-list/ 数据库操作失败：%s",e)
            return_data['msg']='Voice abnormal, Please contact the Voice engineer'
            return return_data,500
        else:
            current_app.logger.info("/code-list/ 查询成功")
            return_data['msg']='Query OK'
            return_data['data']=list[0:-1]
            return_data['total']=list[-1]
            return return_data,200
    else:
        return_data['msg']='Auth Fail'
        return return_data,401




@web_api.route('/api/checkpw',methods=['GET'])
def check_pw():
    request_data=request.args
    decrypt_call_customer_id=request_data.get('customer_id')
    decrypt_call_passwd=request_data.get('password')
    call_passwd=aes_encrypt.encrypt(decrypt_call_passwd).decode('utf8')
    call_customer_id=aes_encrypt.encrypt(decrypt_call_customer_id).decode('utf8')
    passwd_bcsv=dict(event='dtmf',data=dict(dtmf=call_passwd,customer_id=call_customer_id))
    #print(passwd_bcsv)
    # return 'ok',200
    #向账房发起请求验证密码
    response_code=requests.post(dt_domain,json=passwd_bcsv)
    #判断账房回调
    if response_code == 200:
        #成功
        return 'Passwd OK',200
    else:
        return 'Passwd FAIL',401