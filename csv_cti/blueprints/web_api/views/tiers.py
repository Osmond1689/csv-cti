from csv_cti.blueprints.web_api import web_api
from flask import request,current_app,render_template
from csv_cti.blueprints.op.md5_token import encrypt_md5
from csv_cti.blueprints.op.tiers import Tiers_op

#tiers
@web_api.route('/tiers-add/',methods=['POST'])
def tiers_add():
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
        #需要校验参数是否存在
        try:
            Tiers_op.add(r_data)
        except Exception as e:
            current_app.logger.debug("/tiers-add/ 数据库操作失败：%s",e)
            return_data['msg']='Voice abnormal, Please contact the Voice engineer'
            return return_data,500
        else:
            current_app.logger.info("/tiers-add/ 添加成功")
            return_data['msg']='Add OK'
            return return_data,200
    else:
        return_data['msg']='Auth Fail'
        return return_data,401

@web_api.route('/tiers-rm/',methods=['POST'])
def tiers_rm():
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
            Tiers_op.remove(r_data)
        except Exception as e:
            current_app.logger.debug("/tiers-rm/ 数据库操作失败：%s",e)
            return_data['msg']='Voice abnormal, Please contact the Voice engineer'
            return return_data,500
        else:
            current_app.logger.info("/tiers-rm/ 删除成功")
            return_data['msg']='Remove OK'
            return return_data,200
    else:
        return_data['msg']='Auth Fail'
        return return_data,401

@web_api.route('/tiers-list/',methods=['POST'])
def tiers_list():
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
            list=Tiers_op.query(r_data)
        except Exception as e:
            current_app.logger.debug("/tiers-list/ 数据库操作失败：%s",e)
            return_data['msg']='Voice abnormal, Please contact the Voice engineer'
            return return_data,500
        else:
            current_app.logger.info("/tiers-list/ 查询成功")
            return_data['msg']='Query OK'
            return_data['data']=list[0:-1]
            return_data['total']=list[-1]
            return_data['page_size']=r_data['page_size']
            return_data['page_index']=r_data['page_index']
            return return_data,200
    else:
        return_data['msg']='Auth Fail'
        return return_data,401

@web_api.route('/tiers-test/',methods=['GET'])
def tiers_tesy():
    return render_template('socket.html')