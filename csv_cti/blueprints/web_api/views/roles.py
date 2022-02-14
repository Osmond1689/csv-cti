from importlib.abc import PathEntryFinder
from csv_cti.blueprints.web_api import web_api
from flask import request,current_app,render_template
from csv_cti.blueprints.op.md5_token import encrypt_md5

@web_api.route('/roles-list/',methods=['POST'])
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
            // "role":"50001",//可选
            // }
		}
        '''
        #查询role名查询绑定的菜单
        #根据查询的结果查询关系
        #根据关系遍历返回
        try:
            #查询role绑定的菜单
            menus=role_op.query(r_data)
        except Exception as e:
            current_app.logger.debug("/ext-list/ 数据库操作失败：%s",e)
            return_data['msg']='Voice abnormal, Please contact the Voice engineer'
            return return_data,500
        else:
            #根据查询的结果查询关系
            menus_list=menus.split(',')
            data={}
            for i in menus_list:
                #查询i的父
                parent=Menus_op.query('child',i)
                if 
            current_app.logger.info("/ext-list/ 查询成功")
            return_data['msg']='Query OK'
            return_data['data']=data
            return return_data,200
    else:
        return_data['msg']='Auth Fail'
        return return_data,401