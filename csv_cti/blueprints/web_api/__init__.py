from flask import Blueprint

web_api=Blueprint('web_api',__name__,template_folder='templates')

from .views import agents,call,dids,exts,queues,tiers,cdr,groups