from flask import Flask
from datetime import timedelta

from app_login import *
from app_admin import *
from app_home import *
from app_equipment import *

app = Flask(__name__)

app.secret_key = "1234"
app.permanent_session_lifetime = timedelta(minutes=60)

app.register_blueprint(app_login)
app.register_blueprint(app_admin)
app.register_blueprint(app_home)
app.register_blueprint(app_equipment)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")