from csv_cti.blueprints.web_api import web_api
from flask import request,current_app,render_template
from csv_cti.blueprints.op.md5_token import encrypt_md5
from csv_cti.blueprints.op.users import Users_op
from csv_cti.blueprints.op.redis import redis_client


#websocket
# @web_api.route('/users-status/',methods=['GET'])
# def users_status():
#     return render_template('socket.html')
#users
@web_api.route('/users-add/',methods=['POST'])
def users_add():
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
            Users_op.add(r_data)
        except Exception as e:
            current_app.logger.debug("/users-add/ 数据库操作失败：%s",e)
            return_data['msg']='Voice abnormal, Please contact the Voice engineer'
            return return_data,500
        else:
            current_app.logger.info("/users-add/ 添加成功")
            return_data['msg']='Add OK'
            return return_data,200
    else:
        return_data['msg']='Auth Fail'
        return return_data,401

@web_api.route('/users-rm/',methods=['POST'])
def users_rm():
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
            Users_op.remove(r_data)
        except Exception as e:
            current_app.logger.debug("/users-rm/ 数据库操作失败：%s",e)
            return_data['msg']='Voice abnormal, Please contact the Voice engineer'
            return return_data,500
        else:
            current_app.logger.info("/users-rm/ 删除成功")
            return_data['msg']='Remove OK'
            return return_data,200
    else:
        return_data['msg']='Auth Fail'
        return return_data,401
#agent密码修改接口

@web_api.route('/users-list/',methods=['POST'])
def users_list():
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
            list=Users_op.query(r_data)
        except Exception as e:
            current_app.logger.debug("/users-list/ 数据库操作失败：%s",e)
            return_data['msg']='Voice abnormal, Please contact the Voice engineer'
            return return_data,500
        else:
            current_app.logger.info("/users-list/ 查询成功")
            return_data['msg']='Query OK'
            return_data['data']=list[0:-1]
            return_data['total']=list[-1]
            return_data['page_size']=r_data['page_size']
            return_data['page_index']=r_data['page_index']
            return return_data,200
    else:
        return_data['msg']='Auth Fail'
        return return_data,401

@web_api.route('/users-login/',methods=['POST'])
def users_login():
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
        login_data={"user":r_data.get('user'),"auth":r_data.get('y'),"page_index":1,"page_size":10}
        try:
            list=Users_op.query(login_data)
        except Exception as e:
            current_app.logger.debug("/users-login/ 数据库操作失败：%s",e)
            return_data['msg']='Voice abnormal, Please contact the Voice engineer'
            return return_data,500
        else:
            if not list[0]:
                current_app.logger.info("/users-login/ %s 查询失败，座席号不存在",r_data.get('user'))
                return_data['msg']='User Does Not Exist'
                return return_data,404
            else:
                real_user_passwd=list[0].get('password')
        if r_data.get('password')==real_user_passwd:
            return_data['msg']='Login OK'
            return return_data,200
        else:
                current_app.logger.info("/users-login/ %s 查询状态失败，密码错误",r_data.get('user'))
                return_data['msg']='User Password Error'
                return return_data,402
    else:
        return_data['msg']='Auth Fail'
        return return_data,401