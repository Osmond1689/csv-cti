from flask import Blueprint

fs_api=Blueprint('fs_api',__name__,template_folder='templates')

from .views import configuration,dialplan,directory,vars,update_cdr