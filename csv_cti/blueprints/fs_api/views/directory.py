from csv_cti.blueprints.fs_api import fs_api
from flask import request,current_app,make_response,render_template
from csv_cti.blueprints.op.exts import Exts_op


@fs_api.route('/directory',methods=['POST'])
def directory():
    r_token=request.args['tk']
    if r_token in current_app.config['FS_TOKEN']:
        r=request.form
        #print(r)
        sip_auth_username=r.get('user')
        if r.get('Event-Calling-Function')== 'switch_load_network_lists':
            response=make_response(render_template('404.xml'))
            response.headers['Content-Type'] = 'application/xml'
            return response
        elif r.get('Event-Calling-Function')=='config_sofia':
            response=make_response(render_template('404.xml'))
            response.headers['Content-Type'] = 'application/xml'
            return response
        elif sip_auth_username:
                #查询数据库返回xml
                try:
                    ext=Exts_op.query({'group':'1','extnumber':sip_auth_username,'auth':'Y'})
                except AttributeError:
                    response=make_response(render_template('404.xml'))
                    response.headers['Content-Type'] = 'application/xml'
                    return response
                if not ext:
                    response=make_response(render_template('404.xml'))
                    response.headers['Content-Type'] = 'application/xml'
                    return response
                else:
                    response=make_response(render_template('directory.xml',ext=ext))
                    response.headers['Content-Type'] = 'application/xml'
                    return response
        else:
            response=make_response(render_template('404.xml'))
            response.headers['Content-Type'] = 'application/xml'
            return response
    else:
        return 'Auth Fail',401