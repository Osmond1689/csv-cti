from csv_cti.blueprints.fs_api import fs_api
from flask import request,current_app,make_response,render_template
from csv_cti.blueprints.op.queues import Queues_op

@fs_api.route('/queue',methods=['POST'])
def queue():
    r_token=request.args['tk']
    if r_token in current_app.config['FS_TOKEN']:
        if request.values.get('key_value')=='callcenter.conf':
            queues=Queues_op.query({'csv':'Y'})
            response=make_response(render_template('callcenter.conf.xml',params=queues))
            response.headers['Content-Type'] = 'application/xml'
            return response
        else:
            response=make_response(render_template('404.xml'))
            response.headers['Content-Type'] = 'application/xml'
            return response
    else:
        return 'Auth Fail',401
