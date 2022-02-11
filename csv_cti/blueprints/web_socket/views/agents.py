from logging import fatal
import re

from flask import request

from csv_cti.models import agents
from .. import socketio
from flask_socketio import emit
from flask import current_app
from csv_cti.blueprints.op.md5_token import encrypt_md5
from csv_cti.blueprints.op.agents import Agents_op
from csv_cti.blueprints.op.redis import redis_client

#坐席记录表
'''
连接不发日志
'''

@socketio.on('connect')
def connect(json):
    '''
    json
    {
        'token':'',
        'ip':'',
        'agent':'',
        'group':''
    }
    '''
    # current_app.logger.info('%s建立websocket完成')
    #redis_client.lpush(request.sid,1,2)
    emit('connect',{'type':'info','code':'200','data':'connect ok'})
    # if json.get('token') in encrypt_md5(current_app.config['MD5_KEY']):
    #     if json.get('agent') and json.get('ip') and json.get('group'):
    #         '''
    #         Really few parameters
    #         '''
    #         #记录日志
    #         current_app.logger.info('%s建立websocket完成，ip是%s,group是%s',json.get('agent'),json.get('ip'),json.get('group'))
    #         emit('message',{'type':'info','code':'200','data':'connect ok'})
    #     else: 
    #         current_app.logger.info('%s建立websocket失败，ip是%s,group是%s',json.get('agent'),json.get('ip'),json.get('group'))
    #         emit('message',{'type':'error','code':'500','data':'Missing parameters'})
    #         return False
            
    # else:
    #     current_app.logger.info('%s建立websocket失败，ip是%s,group是%s',json.get('agent'),json.get('ip'),json.get('group'))
    #     emit('message',{'type':'error','code':'401','data':'Auth error'})
    #     return False
    


@socketio.on('agent-login')
def agent_login(json):
    '''{
        'token':'',
        'ip':'',
        'agent':'',
        'ext':'',
        'group':''
    }'''
    '''
    redis_client.lpush(json.get('ext'),json.get('agent'),json.get('ip'))
    redis_client.lpush(request.sid,json.get('agent'),json.get('group'))
    '''
    # print('login ....')
    if json.get('token') in encrypt_md5(current_app.config['MD5_KEY']):
        #print('login ....1')
        if json.get('agent') and json.get('ip') and json.get('ext') and json.get('group'):
            #print('login ....2')
            '''
            Really few parameters
            '''
            #记录日志
            if redis_client.exists(json.get('ext')):
                #print('login ....3')
                emit('agent-login',{'type':'error','code':'403','data':'Extension already exists','agent':redis_client.lrange(json.get('ext'),0,-1)[1].decode('utf-8'),'ip':redis_client.lrange(json.get('ext'),0,-1)[0].decode('utf-8')})
                current_app.logger.info('%s坐席签入失败,冲突分机号是%s,ip是%s,坐席是%s',json.get('agent'),json.get('ext'),redis_client.lrange(json.get('ext'),0,-1)[0].decode('utf-8'),redis_client.lrange(json.get('ext'),0,-1)[1].decode('utf-8'))
                
            else:
                r_data={
                "agent":json.get('agent'),
                "ext":json.get('ext'),
                "group":json.get('group')
            }
                try:
                    Agents_op.login(r_data)
                except Exception as e:
                    current_app.logger.debug("/agents-login/ 数据库操作失败：%s",e)
                    current_app.logger.info('%s坐席签入失败原因是%s',e)
                    emit('agent-login',{'type':'error','code':'500','data':'Login Fail','agent':json.get('agent'),'ext':json.get('ext'),'ip':json.get('ip')})
                else:
                    redis_client.lpush(json.get('ext'),json.get('agent'),json.get('ip'))
                    redis_client.lpush(request.sid,json.get('agent'),json.get('group'),json.get('ext'))
                    emit('agent-login',{'type':'info','code':'200','data':'Login ok','agent':json.get('agent'),'ext':json.get('ext'),'ip':json.get('ip')})
                    current_app.logger.info('%s坐席签入,ip是%s,分机号是%s,group是%s',json.get('agent'),json.get('ip'),json.get('ext'),json.get('group'))
        else:
            #print('login ....4')
            emit('agent-login',{'type':'error','code':'500','data':'Missing parameters'})
            current_app.logger.info('login 确少参数')
    else:
        #print('login ....5')
        emit('agent-login',{'type':'error','code':'401','data':'Auth error'})
        current_app.logger.info('%s建立websocket鉴权失败，ip是%s,group是%s',json.get('agent'),json.get('ip'),json.get('group'))
        

@socketio.on('agent-logout')
def agent_logout(json):
    if json.get('token') in encrypt_md5(current_app.config['MD5_KEY']):
        if json.get('agent') and json.get('ip') and json.get('ext'):
            '''
            Really few parameters
            '''
            #记录日志
            r_data={
                "agent":json.get('agent'),
                "group":json.get('group')
            }
            #签出操作
            try:
                Agents_op.logout(r_data)
            except Exception as e:
                current_app.logger.info('%s坐席签出失败原因是%s',e)
                emit('agent-login',{'type':'error','code':'500','data':'Login Fail','agent':json.get('agent'),'group':json.get('group')})
            else:
                try:
                    ext,_,_=redis_client.lrange(request.sid,0,-1)
                    redis_client.delete(ext)
                    redis_client.delete(request.sid)
                except KeyError:
                    current_app.logger.debug('签出坐席失败,坐席未登录')
                    emit('agent-logout',{'type':'error','code':'404','data':'Ext NOt Found'})
                else:
                    current_app.logger.info('坐席签出成功,坐席号%s',json.get('agent'))
                    emit('agent-logout',{'type':'info','code':'200','data':'Logout ok'})
        else:
            emit('agent-logout',{'type':'error','code':'500','data':'Missing parameters'})
    else:
        emit('agent-logout',{'type':'error','code':'401','data':'Auth error'})

@socketio.on('agent-status')
def agent_status():
    if redis_client.exists(request.sid):
        emit('agent-status',{'type':'info','code':'200','data':'Agent-Login'})
    else:
        emit('agent-status',{'type':'info','code':'200','data':'Agent-Logout'})

@socketio.on('disconnect')
def disconnect():
    current_app.logger.info("断开连接")
    try:
        agent,group,ext=redis_client.lrange(request.sid,0,-1)
    except ValueError:
        return current_app.logger.debug('断线后签出坐席失败,坐席未登录')
    else:
        r_data={
                    "agent":agent.decode('utf-8'),
                    "group":group.decode('utf-8')
                }
        try:
            Agents_op.logout(r_data)
        except Exception as e:
            current_app.logger.info('%s坐席签出失败原因是%s',e)
        else:
            try:
                ext,_,_=redis_client.lrange(request.sid,0,-1)
                redis_client.delete(ext)
                redis_client.delete(request.sid)
            except KeyError:
                current_app.logger.debug('断线后签出坐席失败,坐席未登录')
            else:
                current_app.logger.info('断线后坐席签出成功')
    # r_data={
    #             "agent":json.get('agent'),
    #             "group":json.get('group')
    #         }
    # #签出操作
    # try:
    #     Agents_op.logout(r_data)
    # except Exception as e:
    #     current_app.logger.debug("/agents-out/ 数据库操作失败：%s",e)
    # else:
    #     current_app.logger.info("/agents-out/ 签出成功")
    #current_app.logger.info('%s坐席签出,ip是%s,分机号是%s,group是%s',json.get('agent'),json.get('ip'),json.get('ext'),json.get('group'))
