from csv_cti.blueprints.fs_api import fs_api
from flask import request,current_app,make_response,render_template

@fs_api.route('/vars/',methods=['GET'])
def vars():
    r_token=request.args['tk']
    if r_token in current_app.config['FS_TOKEN']:
        response=make_response(render_template('vars.xml',NGINX_URL=current_app.config['NGINX_URL'],MQ=current_app.config['MQ'],PGSQL_DSN=current_app.config['PGSQL_DSN'],PGSQL_CDR_INFO=current_app.config['PGSQL_CDR_INFO'],XML_CURL_SET=current_app.config['XML_CURL_SET'],REDIS_URL=current_app.config['REDIS_URL_LUA']))
        response.headers['Content-Type'] = 'application/xml'
        return response
    else:
        return 'Auth Fail',401