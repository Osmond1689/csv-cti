from . import db
from contextlib import contextmanager
'''
       Column        |          Type           | Collation | Nullable | Default 
----------------------+-------------------------+-----------+----------+---------
 name                 | character varying(255)  |           |          | 
 instance_id          | character varying(255)  |           |          | 
 uuid                 | character varying(255)  |           |          | 
 type                 | character varying(255)  |           |          | 
 contact              | character varying(1024) |           |          | 
 status               | character varying(255)  |           |          | 
 state                | character varying(255)  |           |          | 
 max_no_answer        | integer                 |           | not null | 0
 wrap_up_time         | integer                 |           | not null | 0
 reject_delay_time    | integer                 |           | not null | 0
 busy_delay_time      | integer                 |           | not null | 0
 no_answer_delay_time | integer                 |           | not null | 0
 last_bridge_start    | integer                 |           | not null | 0
 last_bridge_end      | integer                 |           | not null | 0
 last_offered_call    | integer                 |           | not null | 0
 last_status_change   | integer                 |           | not null | 0
 no_answer_count      | integer                 |           | not null | 0
 calls_answered       | integer                 |           | not null | 0
 talk_time            | integer                 |           | not null | 0
 ready_time           | integer                 |           | not null | 0
 external_calls_count | integer                 |           | not null | 0
'''

class Agents(db.Model):
    __tablename__='agents'
    id                   =db.Column(db.Integer,primary_key=True)
    name                 =db.Column(db.String(255))  #1001@default
    group                =db.Column(db.String(255))
    password             =db.Column(db.String(255)) 
    instance_id          =db.Column(db.String(255),default='single_box')  #single_box
    uuid                 =db.Column(db.String(255)) 
    type                 =db.Column(db.String(255),default='callback')  #callback
    contact              =db.Column(db.String(1024)) #user/1001
    status               =db.Column(db.String(255),default='On Break')  #Logged out 座席状态  On Break
    state                =db.Column(db.String(255),default='Waiting')  #Waiting 座席通话状态
    max_no_answer        =db.Column(db.Integer,nullable=False,default=3)  #最大无应答 就会将座席改成On Break
    wrap_up_time         =db.Column(db.Integer,nullable=False,default=30)  #整理时间
    reject_delay_time    =db.Column(db.Integer,nullable=False,default=30)  #拒绝等待时间 
    busy_delay_time      =db.Column(db.Integer,nullable=False,default=30)   #忙碌等待时间 
    no_answer_delay_time =db.Column(db.Integer,nullable=False,default=30)   #未应答等待时间
    last_bridge_start    =db.Column(db.Integer,nullable=False,default=0)   #最后bridge开始时间
    last_bridge_end      =db.Column(db.Integer,nullable=False,default=0)   #最后bridge开始时间
    last_offered_call    =db.Column(db.Integer,nullable=False,default=0)   #最后一次通话结束时间
    last_status_change   =db.Column(db.Integer,nullable=False,default=0)   #最后一次状态更改时间
    no_answer_count      =db.Column(db.Integer,nullable=False,default=0)   #未应答统计
    calls_answered       =db.Column(db.Integer,nullable=False,default=0)   #应答统计
    talk_time            =db.Column(db.Integer,nullable=False,default=0)   #通话时长
    ready_time           =db.Column(db.Integer,nullable=False,default=0)   #准备时长
    external_calls_count =db.Column(db.Integer,nullable=False,default=0)   #呼出统计

    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()  # 事务
        except Exception as e:
            self.session.rollback()  # 回滚
            raise e
    
    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'contact': self.contact,
            'password':self.password,
            'group':self.group
        }
    def to_auth_json(self):
        return{                  
            'name'                 :self.name,
            'group'                :self.group,
            'instance_id'          :self.instance_id,
            'uuid'                 :self.uuid,
            'type'                 :self.type,
            'contact'              :self.contact,
            'status'               :self.status,
            'state'                :self.state,
            'max_no_answer'        :self.max_no_answer,
            'wrap_up_time'         :self.wrap_up_time,
            'reject_delay_time'    :self.reject_delay_time,
            'busy_delay_time'      :self.busy_delay_time,
            'no_answer_delay_time' :self.no_answer_delay_time,
            'last_bridge_start'    :self.last_bridge_start,
            'last_bridge_end'      :self.last_bridge_end,
            'last_offered_call'    :self.last_offered_call,
            'last_status_change'   :self.last_status_change,
            'no_answer_count'      :self.no_answer_count,
            'calls_answered'       :self.calls_answered,
            'talk_time'            :self.talk_time,
            'ready_time'           :self.ready_time,
            'external_calls_count' :self.external_calls_count
        }