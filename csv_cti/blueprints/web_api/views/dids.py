from csv_cti.blueprints.web_api import web_api
from flask import request,current_app
from csv_cti.blueprints.op.md5_token import encrypt_md5
from csv_cti.blueprints.op.dids import Dids_op


#did-queue
@web_api.route('/dids-add/',methods=['POST'])
def dids_add():
    return_data={}
    r_token=request.json.get('token')
    if r_token in encrypt_md5(current_app.config['MD5_KEY']):
        r_data=request.json.get('data')
        '''
        {
			"token":"aecsv@88tech.net",
			"data":[{
                "did":"8888888",//必选
                "queue":"test",//必选
                "group":"C68",//必选 
            }]
		}
        '''
        
        try:
            Dids_op.add(r_data)
        except Exception as e:
            current_app.logger.debug("/dids-add/ 数据库操作失败：%s",e)
            return_data['msg']='Voice abnormal, Please contact the Voice engineer'
            return return_data,500
        else:
            current_app.logger.info("/dids-add/ 添加成功")
            return_data['msg']='Add OK'
            return return_data,200
    else:
        return_data['msg']='Auth Fail'
        return return_data,401

@web_api.route('/dids-rm/',methods=['POST'])
def dids_rm():
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
            Dids_op.remove(r_data)
        except Exception as e:
            current_app.logger.debug("/dids-rm/ 数据库操作失败：%s",e)
            return_data['msg']='Voice abnormal, Please contact the Voice engineer'
            return return_data,500
        else:
            current_app.logger.info("/dids-rm/ 删除成功")
            return_data['msg']='Remove OK'
            return return_data,200
    else:
        return_data['msg']='Auth Fail'
        return return_data,401

@web_api.route('/dids-list/',methods=['POST'])
def dids_list():
    return_data={}
    r_token=request.json.get('token')
    if r_token in encrypt_md5(current_app.config['MD5_KEY']):
        r_data=request.json.get('data')
        '''
        {
			"token":"aecsv@88tech.net",
			"data"://留空字符串查所有
            {
                "queue":"osmond2",//必选
                "group":"C68"//必选
            }
		}
        '''
        try:
            list=Dids_op.query(r_data)
        except Exception as e:
            current_app.logger.debug("/dids-list/ 数据库操作失败：%s",e)
            return_data['msg']='Voice abnormal, Please contact the Voice engineer'
            return return_data,500
        else:
            current_app.logger.info("/dids-list/ 查询成功")
            return_data['msg']='Query OK'
            return_data['data']=list[0:-1]
            return_data['total']=list[-1]
            return return_data,200
    else:
        return_data['msg']='Auth Fail'
        return return_data,401