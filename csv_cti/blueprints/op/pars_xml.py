import xml.etree.cElementTree as ET

def pars_xml(data):
    #print(data)
    root=ET.fromstring(data)
    a=root.findall('./variables/start_stamp')
    b=root.findall('./variables/answer_stamp')
    c=root.findall('./variables/end_stamp')
    d=root.findall('./variables/duration')
    e=root.findall('./variables/billsec')
    if not a:
        return '0','0','0',0,0
    elif not b:
        return a[0].text,'0',c[0].text,d[0].text,e[0].text
    else:
        return a[0].text,b[0].text,c[0].text,d[0].text,e[0].text