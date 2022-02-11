from csv_cti.blueprints.web_api import web_api
from flask import request,current_app
from csv_cti.blueprints.op.md5_token import encrypt_md5
from csv_cti.blueprints.op.exts import Exts_op
#ext
@web_api.route('/exts-add/',methods=['POST'])
def exts_add():
    return_data={}
    r_token=request.json.get('token')
    if r_token in encrypt_md5(current_app.config['MD5_KEY']):
        r_data=request.json.get('data')
        '''
        {
			"token":"aecsv@88tech.net",
			"data":
            [{
            "extnumber":"50008",//必选
            "group":"default",//必选
            "password":"1245678"//必选
            //"extname":"osmond"//可选,不选择和extbumber一样 
            
            }]
		}
        '''
        
        try:
            Exts_op.add(r_data)
        except Exception as e:
            current_app.logger.debug("/ext-add/ 数据库操作失败：%s",e)
            return_data['msg']='Voice abnormal, Please contact the Voice engineer'
            return return_data,500
        else:
            current_app.logger.info("/ext-add/ 添加成功")
            return_data['msg']='Add OK'
            return return_data,200
    else:
        return_data['msg']='Auth Fail'
        return return_data,401

@web_api.route('/exts-rm/',methods=['POST'])
def exts_rm():
    return_data={}
    r_token=request.json.get('token')
    if r_token in encrypt_md5(current_app.config['MD5_KEY']):
        r_data=request.json.get('data')
        '''
        {
			"token":"aecsv@88tech.net",
			"data"://留空查所有
            [{
            "extnumber":"50008",//必选
            "group":"C68"//必选
            //查询不存在的字段异常未捕获
            }]
		}
        '''
        try:
            Exts_op.remove(r_data)
        except Exception as e:
            current_app.logger.debug("/ext-rm/ 数据库操作失败：%s",e)
            return_data['msg']='Voice abnormal, Please contact the Voice engineer'
            return return_data,500
        else:
            current_app.logger.info("/ext-rm/ 删除成功")
            return_data['msg']='Remove OK'
            return return_data,200
    else:
        return_data['msg']='Auth Fail'
        return return_data,401

@web_api.route('/exts-list/',methods=['POST'])
def exts_list():
    return_data={}
    r_token=request.json.get('token')
    if r_token in encrypt_md5(current_app.config['MD5_KEY']):
        r_data=request.json.get('data')
        '''
        {
			"token":"aecsv@88tech.net",
			"data":""
            // {
            // "extnumber":"50001",//可选
            // "group":"C68"//可选
            // }
		}
        '''
        try:
            list=Exts_op.query(r_data)
        except Exception as e:
            current_app.logger.debug("/ext-list/ 数据库操作失败：%s",e)
            return_data['msg']='Voice abnormal, Please contact the Voice engineer'
            return return_data,500
        else:
            current_app.logger.info("/ext-list/ 查询成功")
            return_data['msg']='Query OK'
            return_data['data']=list[0:-1]
            return_data['total']=list[-1]
            return return_data,200
    else:
        return_data['msg']='Auth Fail'
        return return_data,401

@web_api.route('/exts-update/',methods=['POST'])
def exts_update():
    return_data={}
    r_token=request.json.get('token')
    if r_token in encrypt_md5(current_app.config['MD5_KEY']):
        r_data=request.json.get('data')
        '''
        {
			"token":"aecsv@88tech.net",
			"data":
            [{
            "extnumber":"50008",//必选，只识别分机号
            "group":"C68",//必选
            "password":"1245678",//必选
            "extname":"osmond"//必选
            }]
		}
        '''
        try:
            Exts_op.change(r_data)
        except Exception as e:
            current_app.logger.debug("/ext-update/ 数据库操作失败：%s",e)
            return_data['msg']='Voice abnormal, Please contact the Voice engineer'
            return return_data,500
        else:
            current_app.logger.info("/ext-update/ 更新成功")
            return_data['msg']='Update OK'
            return return_data,200
    else:
        return_data['msg']='Auth Fail'
        return return_data,401