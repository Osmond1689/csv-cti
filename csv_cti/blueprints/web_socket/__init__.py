from flask_socketio import SocketIO,emit

socketio=SocketIO(cors_allowed_origins='*')

from .views import agents

