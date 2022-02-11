from csv_cti.blueprints.fs_api import fs_api
from flask import request,current_app
from csv_cti.blueprints.op.pars_xml import pars_xml
from csv_cti.blueprints.op.cdr import Cdr_op
from urllib.parse import unquote
import time

@fs_api.route('/update-cdr',methods=['POST'])
def update_cdr():
    r_token=request.args['tk']
    if r_token in current_app.config['FS_TOKEN']:
        uuid=request.args.get('uuid')
        if uuid[0:2]=='a_':
            return 'OK',200
        else:
            uuid_data=request.form
            for _,v in uuid_data.items():
                bleg_start_stamp,bleg_answer_stamp,bleg_end_stamp,bleg_duration,bleg_billsec=pars_xml(v)
                cdr_info={
                    "bleg_uuid":uuid,
                    "bleg_start_stamp":unquote(bleg_start_stamp,'utf-8'),
                    "bleg_answer_stamp":unquote(bleg_answer_stamp,'utf-8'),
                    "bleg_end_stamp":unquote(bleg_end_stamp,'utf-8'),
                    "bleg_duration":bleg_duration,
                    "bleg_billsec":bleg_billsec}
                try:
                    time.sleep(1)
                    Cdr_op.change(cdr_info)
                except Exception as e:
                    current_app.logger.debug("B腿通话记录写入失败，原因%s",e)
                else:  
                    pass
            return 'OK',200
    else:
        return 'Auth Fail',401