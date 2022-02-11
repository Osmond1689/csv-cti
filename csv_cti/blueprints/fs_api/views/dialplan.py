from csv_cti.blueprints.fs_api import fs_api
from flask import request,current_app,make_response,render_template
from csv_cti.blueprints.op.dids import Dids_op

@fs_api.route('/dialplan',methods=['POST'])
def dialplan():
    r_token=request.args['tk']
    if r_token in current_app.config['FS_TOKEN']:
        if request.values.get('Caller-Context')=='default':
            response=make_response(render_template('dialplan.xml'))
            response.headers['Content-Type'] = 'application/xml'
            return response
        elif request.values.get('Caller-Context')=='public':
            did_queues=Dids_op.query({'csv':'Y'})
            response=make_response(render_template('public.xml',did_queues=did_queues))
            response.headers['Content-Type'] = 'application/xml'
            return response
        else:
            response=make_response(render_template('404.xml'))
            response.headers['Content-Type'] = 'application/xml'
            return response
    else:
        return 'Auth Fail',401