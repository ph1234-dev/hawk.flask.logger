from flask import request, Blueprint, render_template,jsonify, make_response,redirect,url_for

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


# DEFAULT TABLE SETTINGS
table_user_column_settings = TABLE_USER_COLUMN_SETTINGS_DEFAULT = {
    "id": True,
    "name": False,
    "username": False,
    "password": False,
    "created_at": True
}



# API ROUTES

# https://stackoverflow.com/questions/5868786/what-method-should-i-use-for-a-login-authentication-request
# login must be post request
@api.route("/login",methods=["POST"])
@validate_content_type_as_json
def login():
    req = request.json

    user = User.query.filter_by(
        username= req.get('username').strip(),
        password= req.get('password').strip(),
    ).first()
        
    if user is None:
        return "Account does not exist",400 
    else:
        payload = {
            'user': user.username,
            # expire after 3 hours
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=120)
            }
        
        # when you use jwt encode.. always specify the algorithm
        # https://pyjwt.readthedocs.io/en/latest/api.html
        # you have to specify algorithms='thealgo' noe it is not enclosed by brackets
        # https://stackoverflow.com/questions/40179995/pyjwt-returning-invalid-token-signatures
        # as indicated here
        user_token = jwt.encode(
            payload,
            app.config['SECRET_KEY'],
            algorithm="HS256")
        
        # print(user)
        return jsonify(
            id=user.id,
            name=user.name,
            token=user_token)
    

# Doing POST 
# https://sentry.io/answers/flask-getting-post-data/
@api.route("/register",methods=["POST"])
@validate_content_type_as_json
def register():
    req = request.json
    user = User(
        username=req.get('username').strip(),
        password=req.get('password').strip(),
        name=req.get('name').strip()
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



@site.route("/",endpoint="show_users")
def view_recent_logs():
    # user = User.query.order_by(User.created_at.desc()).limit(5).all()
    # count = User.query.count()

    table_user_column_settings = TABLE_USER_COLUMN_SETTINGS_DEFAULT
    page = db.paginate(db.select(User).order_by(User.created_at.desc()),per_page=10)
    return render_template('views/user.jinja', users=page)
    

@site.route("/column/<int:column>",endpoint="sort_columns")
def sort_user_columns(column):
    match column:
        case 0: 
            reverse = not table_user_column_settings['id']
            table_user_column_settings['id'] = reverse

            if table_user_column_settings['id'] == False:
                page = db.paginate(db.select(User).order_by(User.id.desc()),per_page=10)
            else:
                page = db.paginate(db.select(User).order_by(User.id.asc()),per_page=10)
        case 1:
            reverse = not table_user_column_settings['name']
            table_user_column_settings['name'] = reverse
            
            if table_user_column_settings['name'] == False:
                page = db.paginate(db.select(User).order_by(User.name.asc()),per_page=10)
            else:
                page = db.paginate(db.select(User).order_by(User.name.desc()),per_page=10)
        
        case 2:
            reverse = not table_user_column_settings['username']
            table_user_column_settings['username'] = reverse
            
            if table_user_column_settings['username'] == False:
                page = db.paginate(db.select(User).order_by(User.username.asc()),per_page=10)
            else:
                page = db.paginate(db.select(User).order_by(User.username.desc()),per_page=10)
        case 3:
            reverse = not table_user_column_settings['password']
            table_user_column_settings['password'] = reverse
            
            if table_user_column_settings['password'] == False:
                page = db.paginate(db.select(User).order_by(User.password.asc()),per_page=10)
            else:
                page = db.paginate(db.select(User).order_by(User.password.desc()),per_page=10)
        case 4:
            reverse = not table_user_column_settings['created_at']
            table_user_column_settings['created_at'] = reverse
            
            if table_user_column_settings['created_at'] == False:
                page = db.paginate(db.select(User).order_by(User.created_at.asc()),per_page=10)
            else:
                page = db.paginate(db.select(User).order_by(User.created_at.desc()),per_page=10)
    
        case default:
            return "something went wrong"

    return render_template('views/user.jinja', users=page)

    
    
@site.route("/users",methods=['GET','POST'],endpoint="show_searched_user")
def get_searched_user():
    id = request.form.get("id")
    target = db.paginate(db.select(User).filter_by(id=id))
    return render_template('./views/users_available_for_creating_log.jinja',users=target)


@site.route("/delete/<id>",endpoint="user_delete")
def delete_user(id):
    target = User.query.get(id)

    try:
        db.session.delete(target)
        db.session.commit()
        return redirect(url_for('user.site.show_users'))
    except:
        db.session.rollback()
        return "A problem occured when deleting user"
    



# BEGIN SITE ROUTES


# methods is type sensitive use CAPTIALIZE FOR GET/POST/PUT/PATCH
@site.route("/update/<id>",methods=['GET','POST'],endpoint="user_update")
def update_user(id):
    # target = User.query.filter_by(id='').first()
    
    if  request.method == 'GET':
        # render update ui
        target = User.query.get(id)
        return render_template('./views/update_user.jinja',user=target)
    elif request.method == 'POST':
        # render update successful
        target = User.query.get(id)
    
        _username = request.form.get('username')
        _password = request.form.get('password')
        _name = request.form.get('name')

        # target.username = _username
        # if not _username.strip():
        #     return render_template('./views/update_user.jinja',
        #                            user=target,
        #                            error="Username cannot be empty") 
        
        # target.password = _password
        # if not _password.strip():
        #     return render_template('./views/update_user.jinja',
        #                            user=target,
        #                            error="Password cannot be empty") 
        
        # allow name to be empty but not encouraged 
        target.name = _name
        target.username = _username
        target.password = _password

        # print ( f"Target: {target} / Old name: {target.name} / New name: {new_username}")
        try:
            # this all you need
            db.session.commit()
            return redirect(url_for('user.site.show_users'))
        except:
            db.session.rollback()
            return "Something went wrong. Update was not performed"


        # return 'Successful update'

@site.route('/create',endpoint="user_create",methods=['GET','POST'])
def create():
    
    if request.method == 'GET':
        # render_template finds the 
        # template folder . this is a default behavior from flask
        return render_template('./views/create_user.jinja',user=None)
    elif request.method == 'POST':
        
        _username = request.form.get('username')
        _password = request.form.get('password')
        _name = request.form.get('name')


        # if not _username.strip():
        #     return render_template('./views/create_user.jinja',
        #                                error="username cant be empty")
        
        # if not _password.strip():
        #     return render_template('./views/create_user.jinja',
        #                                error="password cant be empty")
            

        
        target = User.query.filter_by(username=_username).first()
        # check if user exist

        # means there is a user that goes by the name user
        if target: 
            # return "target exist"
            return render_template(
                './views/create_user.jinja',
                error=f"Username {_username} already exist.\
                    Please choose a differnet one")
                    
        #         # \ is a part of a new syntax which indicates a split and
        #         # does not break the string
        else:
            
            _user = User(
                username=_username,
                password=_password,
                name=_name
                )
            
            try:
                db.session.add(_user)
                db.session.commit()
                return redirect(url_for('user.site.show_users'))
            except:
                db.session.rollback()

                # suppose user is something like
                # user = { 'name': given-name }
                # you can pass this in as **user in render template
                # such that render_template('path',**user)
                return render_template('./views/create_user.jinja',user=_user)
