from flask import request, Blueprint, render_template,jsonify,redirect,url_for
from config import db, app,validate_content_type_as_json,token_required
from models.models import Log,User
from models.deployment import UniqueTesterIdentifier,UsabilityTestLogs
from sqlalchemy.exc import IntegrityError,NoForeignKeysError


# export log 
log = Blueprint('log',__name__,url_prefix="/log")

# sub blueprint
api = Blueprint('api',__name__,url_prefix="/api")
site = Blueprint('site',__name__)

# connect sub blue plints to main
log.register_blueprint(api)
log.register_blueprint(site)



# DEFAULT TABLE SETTINGS
table_log_column_settings = TABLE_LOG_COLUMN_SETTINGS_DEFAULT = {
    "no": True,
    "user_id": False,
    "message": False,
    "reply": False,
    "created_at": True
}


@api.route("/post",methods=["POST"])
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
    

@api.route("/login",methods=['GET'],endpoint="")
def view_login():
    if request.json:
        _username = request.get("username")
        _password = request.get("password")
    else:
        return "Invalid data received"


# SITE ROUTES


# https://stackoverflow.com/questions/19261833/what-is-an-endpoint-in-flask
@site.route("/",endpoint="show_logs")
def view_recent_logs():
    # read this since we have to use sqlalchmy actual
    # https://docs.sqlalchemy.org/en/20/tutorial/data_select.html
    table_log_column_settings = TABLE_LOG_COLUMN_SETTINGS_DEFAULT
    logs =  db.paginate(
                db.select(Log).order_by(Log.created_at.desc()),
                per_page=10)
    return render_template('views/logs.jinja', logs=logs)



@site.route("/column/<int:column>",endpoint="sort_columns")
def view_ascending_order(column):
    # python switch
    # https://www.freecodecamp.org/news/python-switch-statement-switch-case-example/
    
    if column == 0:
        reverse = not table_log_column_settings["no"] 
        table_log_column_settings["no"] = reverse 

        if reverse == False:
            logs = db.paginate(db.select(Log).order_by(Log.no.asc()), per_page=10)
        else:
            logs = db.paginate(db.select(Log).order_by(Log.no.desc()),per_page=10)
            
    elif column == 1:
        # sort user_id
        
        reverse = not table_log_column_settings["user_id"] 
        table_log_column_settings["user_id"] = reverse 

        if reverse == False:
            logs = db.paginate(db.select(Log).order_by(Log.user_id.asc()),per_page=10)
        else:
            logs = db.paginate(db.select(Log).order_by(Log.user_id.desc()), per_page=10)
        
    elif column == 2:
        # sort messages
        
        reverse = not table_log_column_settings["message"] 
        table_log_column_settings["message"] = reverse 

        if reverse == False:
            logs = db.paginate( db.select(Log).order_by(Log.message.asc()), per_page=10)
        else:
            logs = db.paginate( db.select(Log).order_by(Log.message.desc()),per_page=10)
            
    elif column == 3:

        reverse = not table_log_column_settings["reply"] 
        table_log_column_settings["reply"] = reverse 

        if reverse == False:
            logs = db.paginate(db.select(Log).order_by(Log.reply.asc()), per_page=10)
        else:
            logs = db.paginate( db.select(Log).order_by(Log.reply.desc()), per_page=10)
            
    elif column == 4:
        reverse = not table_log_column_settings["created_at"] 
        table_log_column_settings["created_at"] = reverse 

        if reverse == False:
            logs = db.paginate( db.select(Log).order_by(Log.created_at.asc()), per_page=10)
        else:
            logs = db.paginate( db.select(Log).order_by(Log.created_at.desc()),per_page=10)
        
    return render_template('views/logs.jinja', logs=logs)



@site.route("/delete/<no>",endpoint="delete_log")
def delete_log(no):
    # return " i am deleting " + no
    target = Log.query.filter_by(no=no).first()
    # return f"log {target}"
    try:
        db.session.delete(target)
        db.session.commit()
        return redirect(url_for('log.site.show_logs'))
    except:
        db.session.rollback()
        return "A problem occured when deleting log"


@site.route("/users",endpoint="show_available_users")
def get_users():
    users = db.paginate(
        db.select(User).order_by(User.created_at.desc()),
        per_page=10)
    return render_template('./views/users_available_for_creating_log.jinja',users=users)

@site.route("/create/<id>",endpoint="create_log",methods=['POST','GET'])
def create_user_log(id):

    if request.method == 'GET':

        return render_template('./views/create_log.jinja',target_id=id)
    
    elif request.method == 'POST':

        _message = request.form.get('message')
        _reply = request.form.get('reply')
        _lang = request.form.get('lang') 

        # if not _message.strip():
        #     return render_template('./views/create_log',
        #                 id=id,
        #                 error="User message cannot be empty")

        # if not _reply.strip():
        #     return url_for('log.site.create_log',
        #                 id=id,
        #                 error="Chatbot reply cannot be empty")


        # if not _lang.strip():
        #     return url_for('log.site.create_log',
        #                 id=id,
        #                 error="Predicted language cannot be empty")

        log = Log(
            user_id=id,
            message=_message,
            reply=_reply,
            predicted_message_language=_lang
            )
        
        # print( f"User id: {id} / message: {_message} / reply: {_reply} / lang: {_lang}")
        try:
            db.session.add(log)
            db.session.commit()
            return redirect(url_for('log.site.create_log',id=id))
        except:
            db.session.rollback()
            return "Something went wrong. Could not store log"
        


@site.route("/user_specific_logs/<id>",methods=['GET'],endpoint="get_user_specific_logs")
def get_user_specific_logs(id):
    # logs = Log.query.filter_by(user_id=id).all()
    # logs = User.query.join(Log,User.id==Log.user_id).all()

    # https://www.kevin7.net/post_detail/flask-sqlalchemy-simple-queries
    # join query

    # logs = db.session.query(User).join(Log,Log.user_id==User.id).filter(User.id==id).all()

    # you can actually access the user items when joining by dotting .user 
    # logs = db.session.query(Log).join(User,Log.user_id==User.id).filter(User.id==id).all()
    user = User.query.filter_by(id=id).first()

    logs = db.paginate(
                db.select(Log)
                    .join(User,Log.user_id==User.id)
                    .filter(User.id==id)
                    .order_by(Log.created_at.desc()),
                per_page=10)
    

    return render_template('./views/user_specific_logs.jinja',logs=logs,user=user)


@site.route('/search',methods=['GET','POST'],endpoint="search_by_user")
def search_log_by_user():
    id = request.form.get("id")
    logs = db.paginate(
                db.select(Log)
                    .filter(Log.user_id==id)
                    .order_by(Log.created_at.desc()),
                per_page=10)
    return render_template('views/logs.jinja', logs=logs)



# log
@api.route('/generate_unique_tester_id',methods=['GET','POST'],endpoint="generate_unique_tester_id")
def generate_unique_tester_id():

    
    if request.method == 'GET':
        userCredentials = UniqueTesterIdentifier()
        # print ( userCredentials)
        try:
            db.session.add(userCredentials)
            db.session.commit()
        except:
            db.session.rollback()
            return "Something went wrong in commit database transaction" ,500
        
            # id = userCredentials.id
        return jsonify(msg="Log has been added",id=userCredentials.id)
    
    elif request.method == 'POST':
        req = request.json
        print ( req)
        userCredentials = UniqueTesterIdentifier(
                user_agent=req.get('userAgent'))
        
        # print ( userCredentials)
        try:
            db.session.add(userCredentials)
            db.session.commit()
        except:
            db.session.rollback()
            return "Something went wrong in commit database transaction" ,500
        
            # id = userCredentials.id
        return jsonify(msg="Log has been added",id=userCredentials.id)

# @site.route('/show_unique_tester_id',methods=['GET'],endpoint="show_unique_tester_id")
# def show_unique_tester_id():
#     uniqueIdentifiers = db.paginate(
#                 db.select(UniqueTesterIdentifier)
#                 .order_by(UniqueTesterIdentifier.created_at.desc()),
#                 per_page=10)
#     return render_template('views/show_unique_testers.jinja', records=uniqueIdentifiers)
