from . import db
from contextlib import contextmanager
'''
    csv_address
    call_type
    crm_uuid
    product_code
    agent
    caller_id_name
    caller_id_number
    destination_number
    old_destination_number
    dialplan
    context
    start_stamp
    answer_stamp
    end_stamp
    bleg_start_stamp
    bleg_answer_stamp
    bleg_end_stamp
    duration
    billsec
    bleg_duration
    bleg_billsec
    hangup_cause
    uuid" column="aleg_uuid
    bleg_uuid
    accountcode
    read_codec
    write_codec
    a_answer_bool
    b_answer_bool
    hangup_leg
    record_url
    record_path
'''

class Cdr(db.Model):
    __tablename__='cdr'
    id                   =db.Column(db.Integer,primary_key=True)
    csv_address          =db.Column(db.String(255))
    call_type            =db.Column(db.String(255))
    crm_uuid             =db.Column(db.String(255))
    product_code         =db.Column(db.String(255))
    agent                =db.Column(db.String(255))
    caller_id_name       =db.Column(db.String(255))
    caller_id_number     =db.Column(db.String(255))
    destination_number   =db.Column(db.String(255))
    old_destination_number=db.Column(db.String(255))
    dialplan             =db.Column(db.String(255))
    context              =db.Column(db.String(255))
    aleg_start_stamp     =db.Column(db.String(255))
    aleg_answer_stamp    =db.Column(db.String(255))
    aleg_end_stamp       =db.Column(db.String(255))
    bleg_start_stamp     =db.Column(db.String(255))
    bleg_answer_stamp    =db.Column(db.String(255))
    bleg_end_stamp       =db.Column(db.String(255))
    aleg_duration        =db.Column(db.Integer)
    aleg_billsec         =db.Column(db.Integer)
    bleg_duration        =db.Column(db.Integer)
    bleg_billsec         =db.Column(db.Integer)
    hangup_cause         =db.Column(db.String(255))
    aleg_uuid            =db.Column(db.String(255))
    bleg_uuid            =db.Column(db.String(255))
    accountcode          =db.Column(db.String(255))
    read_codec           =db.Column(db.String(255))
    write_codec          =db.Column(db.String(255))
    a_answer_bool        =db.Column(db.String(255))
    b_answer_bool        =db.Column(db.String(255))
    hangup_leg           =db.Column(db.String(255))
    record_url           =db.Column(db.String(255))
    record_path          =db.Column(db.String(255))
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()  # 事务
        except Exception as e:
            self.session.rollback()  # 回滚
            raise e
    
    def to_json(self):
        d={}
        for c in self.__class__.__table__.columns:
            v = getattr(self, c.name)
            if c.name=="old_destination_number":
                pass
            else:
                d[c.name] = v
        return d