import hashlib
import time,datetime
from typing import MutableSequence
from flask import current_app

def encrypt_md5(old_str):
    utc_now=datetime.datetime.now()
    utc_old_now=(utc_now-datetime.timedelta(minutes=1))
    utc_new_now=(utc_now+datetime.timedelta(minutes=1))

    utc_now_time_array = time.strptime(utc_now.strftime("%Y-%m-%d %H:%M:00"), "%Y-%m-%d %H:%M:00")
    utc_old_now_time_array = time.strptime(utc_old_now.strftime("%Y-%m-%d %H:%M:00"), "%Y-%m-%d %H:%M:00")
    utc_new_now_time_array = time.strptime(utc_new_now.strftime("%Y-%m-%d %H:%M:00"), "%Y-%m-%d %H:%M:00")
    

    time_stamp = str(time.mktime(utc_now_time_array))
    old_time_stamp = str(time.mktime(utc_old_now_time_array))
    new_time_stamp = str(time.mktime(utc_new_now_time_array))
    
    #print(time_stamp,old_time_stamp)
    new_str=old_str+time_stamp[0:10]
    new_str_old=old_str+old_time_stamp[0:10]
    new_str_new=old_str+new_time_stamp[0:10]

    current_app.logger.info('鉴权时间戳是:%s %s',time_stamp[0:10],old_time_stamp[0:10])
    h1=hashlib.md5()
    h2=hashlib.md5()
    h3=hashlib.md5()
    h1.update(new_str.encode(encoding='utf-8'))
    h2.update(new_str_old.encode(encoding='utf-8'))
    h3.update(new_str_new.encode(encoding='utf-8'))
    md5_list=[]
    md5_list.append(h1.hexdigest())
    md5_list.append(h2.hexdigest())
    md5_list.append(h3.hexdigest())
    #添加万能密钥
    md5_list.append('aecsv@88tech.net')
    #调试使用，打印token
    #print(md5_list)
    return md5_list

def encrypt_agent_md5(str):
    h1=hashlib.md5()
    h1.update(str.encode(encoding='utf-8'))
    return h1.hexdigest()

if __name__=='__main__':
    a=encrypt_md5('123')
    print(a)
