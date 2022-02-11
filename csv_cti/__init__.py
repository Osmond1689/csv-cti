from flask import Flask
#from flask_socketio import SocketIO
from csv_cti.blueprints.fs_api import fs_api
from csv_cti.blueprints.web_api import web_api
from csv_cti.models import db
#from csv_cti.blueprints.web_socket import socketio
from csv_cti.blueprints.op.redis import redis_client
import logging
from logging.handlers import TimedRotatingFileHandler



def creat_app():
    app=Flask(__name__)
    app.config.from_object('secret')
    
    app.register_blueprint(fs_api,url_prefix=r'/api')
    app.register_blueprint(web_api,url_prefix=r'/web')
    #app.register_blueprint(web_api)
    #日志
    # 设置最开始的日志级别
    logging.basicConfig(level=logging.DEBUG)
    formatter = logging.Formatter(
        "[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s][%(thread)d] - %(message)s")
    handler = TimedRotatingFileHandler(
        "log/csv.log", when="D", interval=1, backupCount=7,
        encoding="UTF-8", delay=False, utc=True)
    app.logger.addHandler(handler)
    handler.setFormatter(formatter)
    #socketio.init_app(app)
    db.init_app(app)
    redis_client.init_app(app)
    
    
    #创建socket链接
    #创建数据库
    return app
