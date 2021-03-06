#数据库连接字符串
SECRET_KEY='ZAQWSXCDE!@#'
PG_HOST="172.17.0.3"
PG_DATABASE="csv"
PG_USER="csv"
PG_PASSWORD="abc123ABC456!."
SQLALCHEMY_DATABASE_URI='postgresql://'+PG_USER+':'+PG_PASSWORD+'@'+PG_HOST+'/'+PG_USER
SQLALCHEMY_TRACK_MODIFICATIONS=False
SQLALCHEMY_POOL_SIZE=66
SQLALCHEMY_POOL_TIMEOUT=30
REDIS_URL='redis://172.17.0.2:6379/0'
REDIS_URL_LUA='172.17.0.2'
#接口MD5Token密钥
MD5_KEY='DIANXIAOheYUYIN@'
#esl连接字符串
FS_TOKEN=['ZAQ!@#EDCxsw']
#客户号码加密AESCBC算法密钥
AES_KEY='ODY!@#ody123ODY!'
AES_IV='ODY!@#ody123ODY!'
#ESL连接参数
ESL_PASSWD='ClueCon'
ESL_PORT=8021
ESL_DOMAIN='10.71.61.70'
#mq设置
MQ={
    "host":"172.17.0.4",
    "vhost":"csv_event",
    "port":"5672",
    "user":"csv",
    "password":"abc123ABC456!.",
    "exchange":"CSV.Events",
    "type":"topic"
    }
#pgsql连接字符串
PGSQL_DSN="pgsql://host="+PG_HOST+" dbname="+PG_DATABASE+" user="+PG_USER+" password='"+PG_PASSWORD+"' options='-c client_min_messages=NOTICE' application_name='freeswitch'"
PGSQL_CDR_INFO=["host="+PG_HOST+" dbname="+PG_DATABASE+" user="+PG_USER+" password="+PG_PASSWORD+" connect_timeout=10","ODY_CDR"]
#XML-CURL 配置
XML_URL="http://172.17.0.1"
TK="ZAQ!%40%23EDCxsw"
XML_CURL_SET={
    "XML_CURL_DIRECTORY":XML_URL+"/api/directory?tk="+TK,
    "XML_CURL_CONFIG":XML_URL+"/api/queue?tk="+TK,
    "XML_CURL_DIALPLAN":XML_URL+"/api/dialplan?tk="+TK,
    "XML_CDR_UPDATE":XML_URL+"/api/update-cdr?tk="+TK
    
}
#nginx地址
#record_url=$${nginx_url}/$${recordings_dir}/${strftime(%Y%m%d)}/${strftime(%Y%m%d%H%M%S)}_${caller_id_number}.wav
NGINX_URL="http://10.71.55.10"