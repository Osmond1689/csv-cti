import greenswitch


class Send_commands():
    job_status=''
    def __init__(self,cmd_type,esl_domain,esl_port,esl_passwd,crm_uuid=None,extensin_number=None,customer_number=None,agent=None,product_code=None,name=None,group=None) -> None:
        self.crm_uuid=crm_uuid
        self.agent=agent
        self.extensin_number=extensin_number
        self.customer_number=customer_number
        self.product_code=product_code
        self.cmd_type=cmd_type
        self.esl_domain=esl_domain
        self.esl_port=esl_port
        self.esl_passwd=esl_passwd
        self.name=name
        self.group=group
    def send_call(self):
        if self.cmd_type == 'click_on_call':
            cmd='bgapi originate {{crm_uuid={},product_code={},agent={},call_type=click_on_call,leg_type=a,count=1}}user/{} {} XML default'
            new_cmd=cmd.format(self.crm_uuid,self.product_code,self.agent,self.extensin_number,self.customer_number)
            #print(new_cmd)
        elif self.cmd_type == 'binddtmf_call':
            cmd='bgapi originate {{call_type=binddtmf_call,crm_uuid={},product_code={},agent={},call_type=click_on_call,leg_type=a,count=1}}user/{} {} XML default'
            new_cmd=cmd.format(self.crm_uuid,self.product_code,self.agent,self.extensin_number,self.customer_number)
        elif self.cmd_type == 'reload_mod_callcenter':
            new_cmd='bgapi reload mod_callcenter'
        elif self.cmd_type == 'queue reload':
            new_cmd='bgapi callcenter_config queue reload '+self.name+'_'+self.group

        fs=greenswitch.InboundESL(self.esl_domain,self.esl_port,self.esl_passwd)
        
        try:
            fs.connect()
        except Exception as e:
            self.job_status=e
        else:
            bgapi_reponse=fs.send(new_cmd)
            self.job_status=bgapi_reponse.data
            fs.stop()


if __name__ == '__main__':
    host='172.17.0.1'
    port=8021
    password='ClueCon'
    cmd='bgapi originate user/1000 &echo'

    fs=greenswitch.InboundESL(host,port,password)
    
    try:
        fs.connect()
    except Exception as e:
        print(e)
    else:
        bgapi_reponse=fs.send(cmd)
        print(bgapi_reponse.data)
        fs.stop()

