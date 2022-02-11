from csv_cti.models import cdr
from csv_cti.models.cdr import Cdr
from csv_cti.models import db
from sqlalchemy import or_,and_,literal_column

'''
    csv_address
    call_type
    crm_uuid
    product_code
    direction
    caller_id_number
    destination_number
    start_stamp
    billsec 
    hangup_cause
    a_answer_bool
    b_answer_bool
    '''
class Cdr_op():
    @staticmethod
    def query(cdr_info):#只查询group为条件
        query_result_list=[]
        query_result_dict=[]
        fitter_list=[]
        totalDuration=0
        totalBillsec=0
        totalAnswer=0
        # if cdr_info.get('test'):
        #     with Cdr.auto_commit(db):
        #             query_result=Cdr.query(Cdr.crm_uuid.func.string_agg(Cdr)).paginate(cdr_info['page_index'], per_page=cdr_info['page_size'], error_out = False)
        #     for i in query_result.items:
        #         query_result_list.append(i.to_json())
        #     query_result_list.append(query_result.total)
        #     return query_result_list
        if cdr_info.get('group'):
            #接口接group 实际是product_code
            t=Cdr.product_code==cdr_info['group']
            fitter_list.append(Cdr.product_code==cdr_info['group'])
            if cdr_info.get('id'):
                fitter_list.append(Cdr.csv_id==cdr_info['id'])
            if cdr_info.get('call_type'):
                fitter_list.append(Cdr.call_type==cdr_info['call_type'])
            if cdr_info.get('crm_uuid'):
                fitter_list.append(Cdr.crm_uuid==cdr_info['crm_uuid'])
            if cdr_info.get('agent'):
                fitter_list.append(Cdr.agent==cdr_info['agent'])
            if cdr_info.get('caller_id_number'):
                fitter_list.append(Cdr.caller_id_number==cdr_info['caller_id_number'])
            if bjhm:=cdr_info.get('destination_number'):
                if len(bjhm)==32:
                    fitter_list.append(Cdr.destination_number==bjhm)
                else:
                    fitter_list.append(Cdr.old_destination_number==bjhm)
            if cdr_info.get('start_stamp'):
                fitter_list.append(Cdr.aleg_start_stamp>=cdr_info['start_stamp'])
            if cdr_info.get('end_stamp'):
                fitter_list.append(Cdr.aleg_start_stamp<=cdr_info['end_stamp'])
            if cdr_info.get('start_billsec'):
                fitter_list.append(Cdr.bleg_billsec>=cdr_info['start_billsec'])
            if cdr_info.get('end_billsec'):
                fitter_list.append(Cdr.bleg_billsec<=cdr_info['end_billsec'])
            if cdr_info.get('hangup_leg'):
                fitter_list.append(Cdr.hangup_leg==cdr_info['hangup_leg'])
            if cdr_info.get('a_answer_bool'):
                fitter_list.append(Cdr.a_answer_bool==cdr_info['a_answer_bool'])
            if cdr_info.get('b_answer_bool'):
                fitter_list.append(Cdr.b_answer_bool==cdr_info['b_answer_bool'])
            if fitter_list:
                with Cdr.auto_commit(db):
                    origin_data=Cdr.query.filter(and_(*fitter_list)).order_by(Cdr.id.desc())
                    query_result=origin_data.paginate(cdr_info['page_index'], per_page=cdr_info['page_size'], error_out = False)
                for j in origin_data.all():
                    totalDuration=totalDuration+j.aleg_duration
                    totalBillsec=totalBillsec+j.bleg_billsec
                    if j.b_answer_bool =='yes':
                        totalAnswer=totalAnswer+1
                for i in query_result.items:
                    query_result_list.append(i.to_json())
                # query_result_list.append(query_result.total)
                query_result_dict={'data':query_result_list,'total':query_result.total,'totalAnswer':totalAnswer,'totalDuration':totalDuration,'totalBillsec':totalBillsec}
                return query_result_dict
        else:
            if cdr_info.get('id'):
                fitter_list.append(Cdr.csv_id==cdr_info['id'])
            if cdr_info.get('call_type'):
                fitter_list.append(Cdr.call_type==cdr_info['call_type'])
            if cdr_info.get('crm_uuid'):
                fitter_list.append(Cdr.crm_uuid==cdr_info['crm_uuid'])
            if cdr_info.get('agent'):
                fitter_list.append(Cdr.agent==cdr_info['agent'])
            if cdr_info.get('caller_id_number'):
                fitter_list.append(Cdr.caller_id_number==cdr_info['caller_id_number'])
            if bjhm:=cdr_info.get('destination_number'):
                if len(bjhm)==32:
                    fitter_list.append(Cdr.destination_number==bjhm)
                else:
                    fitter_list.append(Cdr.old_destination_number==bjhm)
            if cdr_info.get('start_stamp'):
                fitter_list.append(Cdr.aleg_start_stamp>=cdr_info['start_stamp'])
            if cdr_info.get('end_stamp'):
                fitter_list.append(Cdr.aleg_start_stamp<=cdr_info['end_stamp'])
            if cdr_info.get('start_billsec'):
                fitter_list.append(Cdr.bleg_billsec>=cdr_info['start_billsec'])
            if cdr_info.get('end_billsec'):
                fitter_list.append(Cdr.bleg_billsec<=cdr_info['end_billsec'])
            if cdr_info.get('hangup_leg'):
                fitter_list.append(Cdr.hangup_leg==cdr_info['hangup_leg'])
            if cdr_info.get('a_answer_bool'):
                fitter_list.append(Cdr.a_answer_bool==cdr_info['a_answer_bool'])
            if cdr_info.get('b_answer_bool'):
                fitter_list.append(Cdr.b_answer_bool==cdr_info['b_answer_bool'])
            if fitter_list:
                with Cdr.auto_commit(db):
                    origin_data=Cdr.query.filter(and_(*fitter_list)).order_by(Cdr.id.desc())
                    query_result=origin_data.paginate(cdr_info['page_index'], per_page=cdr_info['page_size'], error_out = False)
                for j in origin_data.all():
                    totalDuration=totalDuration+j.aleg_duration
                    totalBillsec=totalBillsec+j.bleg_billsec
                    if j.b_answer_bool =='yes':
                        totalAnswer=totalAnswer+1
                for i in query_result.items:
                    query_result_list.append(i.to_json())
                # query_result_list.append(query_result.total)
                query_result_dict={'data':query_result_list,'total':query_result.total,'totalAnswer':totalAnswer,'totalDuration':totalDuration,'totalBillsec':totalBillsec}
                return query_result_dict
            else:
                with Cdr.auto_commit(db):
                    origin_data=Cdr.query.filter().order_by(Cdr.id.desc())
                    query_result=origin_data.paginate(cdr_info['page_index'], per_page=cdr_info['page_size'], error_out = False)
                for j in origin_data.all():
                    totalDuration=totalDuration+j.aleg_duration
                    totalBillsec=totalBillsec+j.bleg_billsec
                    if j.b_answer_bool =='yes':
                        totalAnswer=totalAnswer+1
                for i in query_result.items:
                    query_result_list.append(i.to_json())
                # query_result_list.append(query_result.total)
                query_result_dict={'data':query_result_list,'total':query_result.total,'totalAnswer':totalAnswer,'totalDuration':totalDuration,'totalBillsec':totalBillsec}
                return query_result_dict
    @staticmethod
    def change(i):
        with Cdr.auto_commit(db):
            Cdr.query.filter(Cdr.bleg_uuid==i['bleg_uuid']).update({'bleg_start_stamp':i['bleg_start_stamp'],'bleg_answer_stamp':i['bleg_answer_stamp'],'bleg_end_stamp':i['bleg_end_stamp'],'bleg_duration':i['bleg_duration'],'bleg_billsec':i['bleg_billsec']})