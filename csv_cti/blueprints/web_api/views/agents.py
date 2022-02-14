from csv_cti.blueprints.web_api import web_api
from flask import request,current_app,render_template
from csv_cti.blueprints.op.md5_token import encrypt_md5
from csv_cti.blueprints.op.agents import Agents_op
from csv_cti.blueprints.op.redis import redis_client


#websocket
# @web_api.route('/agents-status/',methods=['GET'])
# def agents_status():
#     return render_template('socket.html')
#agents
@web_api.route('/agents-add/',methods=['POST'])
def agents_add():
    return_data={}
    r_token=request.json.get('token')
    if r_token in encrypt_md5(current_app.config['MD5_KEY']):
        r_data=request.json.get('data')
        '''
        {
			"token":"aecsv_cti@88tech.net",
			"data":
            [{
            "name":"50008",         //必选
            "instance_id":"",  //可选，默认single_box
            "uuid":"",         //可选
            "type":"",         //可选 默认callback
            "contact":"50008",      //必选-分机号
            "status":"",       //可选 默认 On_break
            "state":"",         //可选 默认 Waitting
            "group":"C68"          //必选
            "password":"" //新增
            //判断重复
            }]
		}
        '''
        
        try:
            Agents_op.add(r_data)
        except Exception as e:
            current_app.logger.debug("/agents-add/ 数据库操作失败：%s",e)
            return_data['msg']='Voice abnormal, Please contact the Voice engineer'
            return return_data,500
        else:
            current_app.logger.info("/agents-add/ 添加成功")
            return_data['msg']='Add OK'
            return return_data,200
    else:
        return_data['msg']='Auth Fail'
        return return_data,401

@web_api.route('/agents-rm/',methods=['POST'])
def agents_rm():
    return_data={}
    r_token=request.json.get('token')
    if r_token in encrypt_md5(current_app.config['MD5_KEY']):
        r_data=request.json.get('data')
        '''
        {
			"token":"97d5fc0bdfc499fc8a008199cab1be53",
			"data":[{
                "name":xxx,必选参数
                "group":xxxx,必选参数
            }]
		}
        '''
        try:
            Agents_op.remove(r_data)
        except Exception as e:
            current_app.logger.debug("/agents-rm/ 数据库操作失败：%s",e)
            return_data['msg']='Voice abnormal, Please contact the Voice engineer'
            return return_data,500
        else:
            current_app.logger.info("/agents-rm/ 删除成功")
            return_data['msg']='Remove OK'
            return return_data,200
    else:
        return_data['msg']='Auth Fail'
        return return_data,401
#agent密码修改接口

@web_api.route('/agents-list/',methods=['POST'])
def agents_list():
    return_data={}
    r_token=request.json.get('token')
    if r_token in encrypt_md5(current_app.config['MD5_KEY']):
        r_data=request.json.get('data')
        '''
       {
			"token":"aecsv_cti@88tech.net",
			"data"://留空字符串查所有
            {
                "name":"osmond",//可选
                "group":"C68"//可选
            }
		}
        '''
        try:
            list=Agents_op.query(r_data)
        except Exception as e:
            current_app.logger.debug("/agents-list/ 数据库操作失败：%s",e)
            return_data['msg']='Voice abnormal, Please contact the Voice engineer'
            return return_data,500
        else:
            current_app.logger.info("/agents-list/ 查询成功")
            return_data['msg']='Query OK'
            return_data['data']=list[0:-1]
            return_data['total']=list[-1]
            return_data['page_size']=r_data['page_size']
            return_data['page_index']=r_data['page_index']
            return return_data,200
    else:
        return_data['msg']='Auth Fail'
        return return_data,401

@web_api.route('/agents-login/',methods=['POST'])
def agents_login():
    '''
       {
			"token":"aecsv_cti@88tech.net",
            "data":
            {
                "agent":"osmond",
                "ip":"",
                "agent-passwd:"",//md5加密，由用户手动输入
                "group":"P91"
            }
		}
        '''
    return_data={}
    r_token=request.json.get('token')
    if r_token in encrypt_md5(current_app.config['MD5_KEY']):
        r_data=request.json.get('data')
        login_data={"group":r_data.get('group'),"name":r_data.get('agent'),"page_index":1,"page_size":10}
        try:
            list=Agents_op.query(login_data)
        except Exception as e:
            current_app.logger.debug("/agents-login/ 数据库操作失败：%s",e)
            return_data['msg']='Voice abnormal, Please contact the Voice engineer'
            return return_data,500
        else:
            if not list[0]:
                current_app.logger.info("/agents-status/ %s 查询失败，座席号不存在",r_data.get('agent'))
                return_data['msg']='Agent Does Not Exist'
                return return_data,404
            else:
                real_agent_passwd=list[0].get('password')
        if r_data.get('agent_password')==real_agent_passwd:
            return_data['msg']='Login OK'
            return return_data,200
        else:
                current_app.logger.info("/agents-status/ %s 查询状态失败，密码错误",r_data.get('agent'))
                return_data['msg']='Agent Password Error'
                return return_data,402
    else:
        return_data['msg']='Auth Fail'
        return return_data,401

@web_api.route('/agents-bind/',methods=['POST'])
def agents_bind():
    return_data={}
    r_token=request.json.get('token')
    if r_token in encrypt_md5(current_app.config['MD5_KEY']):
        r_data=request.json.get('data')
        if r_data.get('agent')  and r_data.get('ext') and r_data.get('group') and r_data.get('agent_password'):
            '''
        {
                "token":"aecsv_cti@88tech.net",
                "data":
                {
                    "ip":"",
                    "agent":"osmond",
                    "ext":"50001",
                    "group":"C68",
                    "agent_password":"",
                    "ack":'1'//可选
                }
            }
            '''
            login_data={"group":r_data.get('group'),"name":r_data.get('agent'),"page_index":1,"page_size":10}
            try:
                list=Agents_op.query(login_data)
            except Exception as e:
                current_app.logger.debug("/agents-login/ 数据库操作失败：%s",e)
                return_data['msg']='Voice abnormal, Please contact the Voice engineer'
                return return_data,500
            else:
                if not list[0]:
                    current_app.logger.info("/agents-login/ %s 签入失败，座席号不存在",r_data.get('agent'))
                    return_data['msg']='Agent Does Not Exist'
                    return return_data,404
                else:
                    real_agent_passwd=list[0].get('password')
            if r_data.get('agent_password')==real_agent_passwd:
                if redis_client.exists(r_data.get('ext')+'_ext') and r_data.get('ack') != '1':
                    return_data['msg']='The extension number has been bound'
                    return_data['data']={'agent':redis_client.lrange(r_data.get('ext')+'_ext',0,-1)[1].decode('utf-8'),'ip':redis_client.lrange(r_data.get('ext')+'_ext',0,-1)[0].decode('utf-8')}
                    return return_data,403
                else:
                    try:
                        Agents_op.login(r_data)
                    except Exception as e:
                        current_app.logger.debug("/agents-login/ 数据库操作失败：%s",e)
                        return_data['msg']='Voice abnormal, Please contact the Voice engineer'
                        return return_data,500
                    else:
                        ip=request.remote_addr
                        #避免key重复，当座席号和分机号一致时就会出现重复
                        redis_client.hset(r_data.get('agent')+'_agent',r_data.get('agent'),r_data.get('ext'))
                        redis_client.lpush(r_data.get('ext')+'_ext',r_data.get('agent'),ip)
                        current_app.logger.info("/agents-login/ %s 签入成功",r_data.get('agent'))
                        return_data['msg']='Bind OK'
                        return return_data,200
            else:
                current_app.logger.info("/agents-Bind/ %s 签入失败，密码错误",r_data.get('agent'))
                return_data['msg']='Agent Password Error'
                return return_data,402
        else:
            return_data['msg']='Missing parameters'
            current_app.logger.info('Bind 确少参数')
            return return_data,502
    else:
        return_data['msg']='Auth Fail'
        return return_data,401

@web_api.route('/agents-unbind/',methods=['POST'])
def agents_unbind():
    return_data={}
    r_token=request.json.get('token')
    if r_token in encrypt_md5(current_app.config['MD5_KEY']):
        r_data=request.json.get('data')
        '''
       {
			"token":"aecsv_cti@88tech.net",
            "data":
            {
                "agent":"osmond",//可选
                "group":"C68"//可选
            }
		}
        '''
        login_data={"group":r_data.get('group'),"name":r_data.get('agent'),"page_index":1,"page_size":10}
        try:
            list=Agents_op.query(login_data)
        except Exception as e:
            current_app.logger.debug("/agents-logout/ 数据库操作失败：%s",e)
            return_data['msg']='Voice abnormal, Please contact the Voice engineer'
            return return_data,500
        else:
            if not list[0]:
                current_app.logger.info("/agents-logout/ %s 签出失败，座席号不存在",r_data.get('agent'))
                return_data['msg']='Agent Does Not Exist'
                return return_data,404
            else:
                real_agent_passwd=list[0].get('password')
        if r_data.get('agent_password')==real_agent_passwd:
            try:
                Agents_op.logout(r_data)
            except Exception as e:
                current_app.logger.debug("/agents-out/ 数据库操作失败：%s",e)
                return_data['msg']='Voice abnormal, Please contact the Voice engineer'
                return return_data,500
            else:
                current_app.logger.info("/agents-out/ 签出成功")
                try:
                    ext=redis_client.hget(r_data.get('agent')+'_agent',r_data.get('agent')).decode('utf-8')
                except AttributeError:
                    return_data['msg']='Agent Not Logged In'
                    return return_data,404
                else:
                    redis_client.hdel(r_data.get('agent')+'_agent',r_data.get('agent'))
                    redis_client.delete(ext+'_ext')
                    return_data['msg']='Logout OK'
                    return return_data,200
        else:
            current_app.logger.info("/agents-logout/ %s 签出失败，密码错误",r_data.get('agent'))
            return_data['msg']='Agent Password Error'
            return return_data,402
    else:
        return_data['msg']='Auth Fail'
        return return_data,401

@web_api.route('/agents-status/',methods=['POST'])
def agents_status():
    '''
       {
			"token":"aecsv_cti@88tech.net",
            "data":
            {
                "agent":"osmond",
                "ip":"",
                "agent-passwd:"",//md5加密，由用户手动输入
                "group":"P91"
            }
		}
        '''
    return_data={}
    r_token=request.json.get('token')
    if r_token in encrypt_md5(current_app.config['MD5_KEY']):
        r_data=request.json.get('data')
        login_data={"group":r_data.get('group'),"name":r_data.get('agent'),"page_index":1,"page_size":10}
        try:
            list=Agents_op.query(login_data)
        except Exception as e:
            current_app.logger.debug("/agents-login/ 数据库操作失败：%s",e)
            return_data['msg']='Voice abnormal, Please contact the Voice engineer'
            return return_data,500
        else:
            if not list[0]:
                current_app.logger.info("/agents-status/ %s 查询失败，座席号不存在",r_data.get('agent'))
                return_data['msg']='Agent Does Not Exist'
                return return_data,404
            else:
                real_agent_passwd=list[0].get('password')
        if r_data.get('agent_password')==real_agent_passwd:
            ip=request.remote_addr
            if redis_client.hexists(r_data.get('agent')+'_agent',r_data.get('agent')):
                ext=redis_client.hget(r_data.get('agent')+'_agent',r_data.get('agent')).decode('utf-8')
                last_ip=redis_client.lrange(ext+'_ext',0,-1)[0].decode('utf-8')
                redis_client.lset(ext+'_ext',0,ip)
                return_data['msg']='Already Login'
                return_data['data']={'agent':r_data.get('agent'),'ext':ext,'ip':last_ip}
                return return_data,200
            else:
                return_data['msg']='Not Found'
                return return_data,406
        else:
                current_app.logger.info("/agents-status/ %s 查询状态失败，密码错误",r_data.get('agent'))
                return_data['msg']='Agent Password Error'
                return return_data,402
    else:
        return_data['msg']='Auth Fail'
        return return_data,401