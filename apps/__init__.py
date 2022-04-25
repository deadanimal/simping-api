import requests
import json
import time
import os

from flask import Flask, render_template, flash, request, redirect, request_finished, session, jsonify
from flask_recaptcha import ReCaptcha
from flask_sqlalchemy import SQLAlchemy
from decouple import config
from web3.auto import w3
from eth_account.messages import encode_defunct
from authy.api import AuthyApiClient
from flask_migrate import Migrate
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_security import Security, login_required, \
     SQLAlchemySessionUserDatastore
from flask_mail import Mail



app = Flask(__name__)


app.config['DEBUG'] = config('DEBUG')
app.config['BASE_DIR'] = os.path.abspath(os.path.dirname(__file__))  
app.config['DATABASE_CONNECT_OPTIONS'] = {}
app.config['CSRF_SESSION_KEY'] = config('SECRET_KEY')
app.config['SECRET_KEY'] = config('SECRET_KEY')
app.config['CSRF_SESSION_KEY'] = config('SECRET_KEY')
app.config['CSRF_ENABLED'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = config('DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CSRF_ENABLED'] = True
app.config['THREADS_PER_PAGE'] = 2
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_TRACKABLE'] = True
app.config['SECURITY_CONFIRMABLE'] = True
app.config['SECURITY_RECOVERABLE'] = True
app.config['SECURITY_PASSWORD_SALT'] = config('SECRET_KEY')
app.config['MAIL_SERVER'] = 'smtp.purelymail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_DEBUG'] = True
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'simping@app.pipeline.com.my'
app.config['MAIL_PASSWORD'] = 'VsTu9a9Ek3$Xp*pbVq8N'
app.config['MAIL_DEFAULT_SENDER'] = app.config['MAIL_USERNAME']


recaptcha = ReCaptcha(app) 
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)
mail = Mail(app)


from apps.user.models import user_datastore
security = Security(app, user_datastore)

CORS(app)



@app.route('/')
def home():
    data_ = {
        'ts': int(time.time())
    }
    return jsonify(data_)


@app.route('/instagram-redirect')
def instagram_redirect():
    code = request.args.get('code')
    code = code.replace("#_", "")

    files = {
        'client_id': (None, config('INSTAGRAM_APP_ID')),
        'client_secret': (None, config('INSTAGRAM_APP_SECRET')),
        'grant_type': (None, 'authorization_code'),
        'redirect_uri': (None, 'https://simping-api.onrender.com/instagram-redirect'),
        'code': (None, code),
    }

    response = requests.post('https://api.instagram.com/oauth/access_token', files=files)
    json_data = response.json()
    redirected_url = 'https://simping.org/instagram-login?access_token=' + json_data['access_token'] + '&user_id=' + json_data['user_id']
    return redirect(redirected_url)

# @app.route('/about')
# def about():
#     return render_template('about.html')

# from apps.collection.controllers import collection_bp as collection_module
# app.register_blueprint(collection_module)


db.create_all()
