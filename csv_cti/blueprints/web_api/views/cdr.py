from csv_cti.blueprints.web_api import web_api
from flask import request,current_app
from csv_cti.blueprints.op.md5_token import encrypt_md5
from csv_cti.blueprints.op.cdr import Cdr_op


@web_api.route('/cdr-list/',methods=['POST'])
def cdr_list():
    return_data={}
    r_token=request.json.get('token')
    if r_token in encrypt_md5(current_app.config['MD5_KEY']):
        r_data=request.json.get('data')
        '''
        {
			"token":"aecsv@88tech.net",
			"data":
            {
                csv_address
                call_type
                crm_uuid
                product_code
                direction
                caller_id_number
                destination_number
                start_stamp
                billsec 
                hangup_cause
                a_answer_bool
                b_answer_bool
                "group":"C68"//必选
            }
		}
        '''
        try:
            dict=Cdr_op.query(r_data)
        except Exception as e:
            current_app.logger.debug("/cdr-list/ 数据库操作失败：%s",e)
            return_data['msg']='Voice abnormal, Please contact the Voice engineer'
            return return_data,500
        else:
            current_app.logger.info("/cdr-list/ 查询成功")
            return_data['msg']='Query OK'
            return_data['data']=dict.get('data')
            return_data['total']=dict.get('total')
            return_data['totalDuration']=dict.get('totalDuration')
            return_data['totalBillsec']=dict.get('totalBillsec')
            return_data['totalAnswer']=dict.get('totalAnswer')
            return_data['page_size']=r_data['page_size']
            return_data['page_index']=r_data['page_index']
            return return_data,200
    else:
        return_data['msg']='Auth Fail'
        return return_data,401
