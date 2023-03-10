from flask import request, Blueprint, render_template,jsonify, make_response
from config import db,app,validate_content_type_as_json
from models.models import User
from sqlalchemy.exc import IntegrityError,NoForeignKeysError

from flask import Blueprint

# jwt and datetime are for token config

import jwt
import datetime

# the name of the blueprint is user
# https://www.youtube.com/watch?v=pjVhrIJFUEs
# the blue print name here 'user' will be used by the url_for('user.[the-endpoint-name]')
user = Blueprint('user',__name__,url_prefix="/user")
# url_prefix="" add this


# sub blueprint
api = Blueprint('api',__name__,url_prefix="/api")
site = Blueprint('site',__name__)

user.register_blueprint(api)
user.register_blueprint(site)

# https://stackoverflow.com/questions/5868786/what-method-should-i-use-for-a-login-authentication-request
# login must be post request
@api.route("/login",methods=["post"])
@validate_content_type_as_json
def login():
    req = request.json

    user = User.query.filter_by(
        username= req.get('username'),
        password= req.get('password'),
    ).first()
        
    if user is None:
        return "Account does not exist",400 
    else:

        user_token = jwt.encode({
            'user': user.username,
            # expire after 3 hours
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=120)
            },
            app.config['SECRET_KEY'])
        
        # print(user)
        return jsonify(
            id=user.id,
            name=user.name,
            token=user_token)

# Doing POST 
# https://sentry.io/answers/flask-getting-post-data/
@api.route("/register",methods=["post"])
@validate_content_type_as_json
def register():
    req = request.json
    user = User(
        username=req.get('username'),
        password=req.get('password'),
        name=req.get('name')
        )

    # read this for exception handling
    # https://www.youtube.com/watch?v=P-Z1wXFW4Is
    try:
        # if multiple use db.session.add_all([obj1,obj2..])
        # https://www.youtube.com/watch?v=VVX7JIWx-ss
        # time stamp at 1:42

        db.session.add(user)
        # commit the final save
        db.session.commit()

        user = User.query.filter_by(
                username=req.get('username'),
                password=req.get('password'),
            ).first()

        return jsonify(id=user.id, name=user.name)
            # return "User has been added",201

    except IntegrityError:
        # undo the session added
        # this is mandatory you to maintain
        # consistency
        db.session.rollback()
        # use the generic error code 500 for database errors
        return "The User already exist", 500

@site.route("/records",endpoint="show_users")
def view_recent_logs():
    user = User.query.order_by(User.created_at.desc()).limit(5).all()
    count = User.query.count()
    return render_template('views/user.jinja', users=user,count=count)
    
