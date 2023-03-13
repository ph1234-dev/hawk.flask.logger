from flask import request, Blueprint, render_template,jsonify
from config import db, app,validate_content_type_as_json,token_required
from models.models import Log
from sqlalchemy.exc import IntegrityError,NoForeignKeysError


# export log 
log = Blueprint('log',__name__,url_prefix="/log")

# sub blueprint
api = Blueprint('api',__name__,url_prefix="/api")
site = Blueprint('site',__name__)

# connect sub blue plints to main
log.register_blueprint(api)
log.register_blueprint(site)

@api.route("/post",methods=["post"])
@validate_content_type_as_json
@token_required
def post_log():
        
    req = request.json
        
    log = Log(
        user_id=req.get("user_id"),
        message=req.get("message"),
        reply=req.get("reply"),
        predicted_message_language=req.get("predicted_message_language")
        )

    try:
        db.session.add(log)
        db.session.commit()
    except:
        db.session.rollback()
        return "Something went wrong in commit database transaction"

    return jsonify(msg="Log has been added")
    


# https://stackoverflow.com/questions/19261833/what-is-an-endpoint-in-flask
@site.route("/recent",endpoint="show_recent_logs")
def view_recent_logs():
    count = 5
    logs = Log.query.order_by(Log.created_at.desc()).limit(count).all()
    return render_template('views/logs.jinja', logs=logs,count=count)
    

@api.route("/login",methods=['GET'],endpoint="")
def view_login():
    if request.json:
        _username = request.get("username")
        _password = request.get("password")
    else:
        return "Invalid data received"