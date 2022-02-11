'''
    <param name="strategy" value="longest-idle-agent"/>
    <param name="moh-sound" value="$${hold_music}"/>
    <param name="record-template" value="$${recordings_dir}/${strftime(%Y-%m-%d-%H-%M-%S)}.${destination_number}.${caller_id_number}.${uuid}.wav"/>
    <param name="time-base-score" value="system"/><!--时基分数 queue or system-->
    <param name="max-wait-time" value="0"/>
    <param name="max-wait-time-with-no-agent" value="0"/>
    <param name="max-wait-time-with-no-agent-time-reached" value="5"/>
    <param name="tier-rules-apply" value="false"/>
    <param name="tier-rule-wait-second" value="300"/>
    <param name="tier-rule-wait-multiply-level" value="true"/>
    <param name="tier-rule-no-agent-no-wait" value="false"/>
    <param name="discard-abandoned-after" value="60"/>
    <param name="abandoned-resume-allowed" value="false"/>
'''
from . import db
from contextlib import contextmanager

class Queues(db.Model):
    __tablename__="queues"
    id                                              = db.Column(db.Integer,primary_key=True)
    name                                            = db.Column(db.String(10))
    group                                           = db.Column(db.String(10))
    strategy                                        = db.Column(db.String(255),default='longest-idle-agent')
    moh_sound                                       = db.Column(db.String(255),default='$${hold_music}')
    record_template                                 = db.Column(db.String(255),default='$${recordings_dir}/${strftime(%Y-%m-%d-%H-%M-%S)}.${destination_number}.${caller_id_number}.${uuid}.wav')
    time_base_score                                 = db.Column(db.String(10),default='system')#时基分数 queue or system
    max_wait_time                                   = db.Column(db.Integer,default=60)
    max_wait_time_with_no_agent                     = db.Column(db.Integer,default=60)
    max_wait_time_with_no_agent_time_reached        = db.Column(db.Integer,default=5)
    tier_rules_apply                                = db.Column(db.String(10),default='false')
    tier_rule_wait_second                           = db.Column(db.Integer,default=300)
    tier_rule_wait_multiply_level                   = db.Column(db.String(10),default='true')
    tier_rule_no_agent_no_wait                      = db.Column(db.String(10),default='false')
    discard_abandoned_after                         = db.Column(db.Integer,default=60)
    abandoned_resume_allowed                        = db.Column(db.String(10),default='false')
    '''
    calls_answered
    calls_abandoned
    ring_progressively_delay
    skip_agents_with_external_calls
    agent_no_answer_status
    '''


    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()  # 事务
        except Exception as e:
            self.session.rollback()  # 回滚
            raise e
    # def to_json(self):
    #     d={}
    #     for c in self.__class__.__table__.columns:
    #         v = getattr(self, c.name)
    #         d[c.name] = v
    #     return d
    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'group':self.group.upper()
        }