from csv_cti.models.users import Users
from csv_cti.models import db
from flask import current_app


class Users_op():
    
    '''
    ext={
            user= db.Column(db.String(10))
            password= db.Column(db.String(10))
            group= db.Column(db.String(30))
            agent= db.Column(db.String(30))
            role= db.Column(db.String(10))
        }
    '''
    @staticmethod
    def add(user_info_list):#分机信息map组成列表
        add_list=[]
        for i in user_info_list:
            add_list.append(Users(group=i['group'].upper(),user=i['user'],password=i['password'],agent=i['agent'].lower(),role=i['role']))
            current_app.logger.info("用户添加接口调用成功:%s:%s",i['user'],i['group'])
        with Users.auto_commit(db):
            db.session.add_all(add_list)

    @staticmethod
    def remove(user_info_list):#分机号,doamin组成的map 列表
        with Users.auto_commit(db):
            for i in user_info_list:
                a=Users.query.filter(Users.group==i['group'].upper(),Users.user==i['user']).first()
                if a:
                    db.session.delete(a)

        
    @staticmethod
    def change(user_info_list):#分机号,doamin组成的map 列表
        with Users.auto_commit(db):
            for i in user_info_list:
                #所有参数必传
                Users.query.filter(Users.extnumber==i['user'],Users.group==i['group'].upper()).update({'password':i['password'],'agent':i['agent'].lower(),'role':i['role']})
                
    @staticmethod
    def query(user_info):#group,extname组成的map三种查询结果  group extnumber 全部
        query_result_list=[]
        if user_info.get('login') == 'y':
            query_result=Users.query.filter(Users.user==user_info['user']).order_by(Users.id.desc()).paginate(user_info['page_index'], per_page=user_info['page_size'], error_out = False)
            for i in query_result.items:
                query_result_list.append(i.to_auth_json())
            query_result_list.append(query_result.total)
            return query_result_list
        else:
            if user_info.get('group'):
                if user_info.get('user'):
                        query_result=Users.query.filter(Users.user==user_info['user']).order_by(Users.id.desc()).paginate(user_info['page_index'], per_page=user_info['page_size'], error_out = False)
                        for i in query_result.items:
                            query_result_list.append(i.to_json())
                        query_result_list.append(query_result.total)
                        return query_result_list
                else:
                    query_result=Users.query.filter(Users.group==user_info['group'].upper()).order_by(Users.id.desc()).paginate(user_info['page_index'], per_page=user_info['page_size'], error_out = False)
                    for i in query_result.items:
                        query_result_list.append(i.to_json())
                    query_result_list.append(query_result.total)
                    return query_result_list
            else:
                query_result=Users.query.filter().order_by(Users.id.desc()).paginate(user_info['page_index'], per_page=user_info['page_size'], error_out = False)
                for i in query_result.items:
                    query_result_list.append(i.to_json())
                query_result_list.append(query_result.total)
                return query_result_list
