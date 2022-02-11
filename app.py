#from csv_cti.blueprints.web_socket import socketio
from csv_cti import creat_app
from csv_cti.models import db



app=creat_app()
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run()