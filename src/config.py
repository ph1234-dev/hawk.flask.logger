# FOLLOW THIS TO AVOID CIRCULAR IMPORTS
# https://kimlehtinen.com/flask-database-migrations-using-flask-migrate/#:~:text=Next%20step%20is%20to%20actually,always%20apply%20the%20latest%20changes.&text=If%20we%20now%20check%20our,to%20track%20migration%20version%20numbers.
from flask import Flask,request,make_response,jsonify

# https://kimlehtinen.com/flask-database-migrations-using-flask-migrate/#:~:text=Next%20step%20is%20to%20actually,always%20apply%20the%20latest%20changes.&text=If%20we%20now%20check%20our,to%20track%20migration%20version%20numbers.
from flask_migrate import Migrate

# https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/quickstart/
from flask_sqlalchemy import SQLAlchemy

# enable cross origin response
from flask_cors import CORS

# use this to create decorators
from functools import wraps

# import machine learning model from sklearn from joblib
import joblib 

# import this which require pip install pyjwt
# https://www.youtube.com/watch?v=J5bIPtEbS0Q&t=397s
import jwt 


# loads the saved model from sklearn 
model = joblib.load('./ml/nb.model')

# load the feature vectorizer saved from sklearn
# if this is numerical then we can just straight np.array([1,2,3]).reshape(-1,1)
feature_vectorizer = joblib.load('./ml/nb.vectorizer')


# input = ["ano pwede kong gawin pag may sakit"]
# res = feature_vectorizer.transform(input)
# lang_predicted = model.predict(res)
# print(f"Testing model: {lang_predicted}")

# initialize the app with the extension


# create the app
app = Flask(__name__)

# enable cors
CORS(app,supports_credentials=True)


# db_path = os.path.join(os.path.dirname(__file__), '/var/config-instance/hawk.db')
# db_uri = 'sqlite:///{}'.format(db_path)
# app.config["SQLALCHEMY_DATABASE_URI"] = db_uri

# initialize the app with the extension
# use this when using sqlite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hawk.db"

# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:root@localhost:5432/hawk"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# read for additional databases
# https://www.youtube.com/watch?v=SB5BfYYpXjE
# app.config['SQLALCHEMY_BINDS'] = {
#     'postgresql': 'postgresql://postgres:root@localhost:5432/hawk'
# }

#setting jwt 
# https://www.youtube.com/watch?v=J5bIPtEbS0Q&t=397s
app.config['SECRET_KEY'] = 'hawk.io'

# initialize the app with the extension
db = SQLAlchemy(app)    


# https://kimlehtinen.com/flask-database-migrations-using-flask-migrate/#:~:text=Next%20step%20is%20to%20actually,always%20apply%20the%20latest%20changes.&text=If%20we%20now%20check%20our,to%20track%20migration%20version%20numbers.
migrate = Migrate(app, db)



# DO THIS AFTER migrate = Migrate(app,db)

# step1: Initializing database repository (if not yet else proceed to step 2)
# if repository already exist then proceed to step 2
# py -m flask db init

# step2: Create Migration
# py -m flask db migrate

#step3: 
#py -m flask db upgrade


# FLASK BY DEFAULT HAS ITS FOREIGN KEYS DISABLED SO.. YOU HAVE TO ENABLE THIS
# you have to call this everytime you instantiate a connection
# https://gist.github.com/asyd/a7aadcf07a66035ac15d284aef10d458

#to manually enforce foreign key for sqlite
# you have to go to directory then sqlite3 [dbname].db
#when inside sqlite you can run PRAGMA foreign_keys = ON;

# Ensure FOREIGN KEY for sqlite3
if 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']:
    def _fk_pragma_on_connect(dbapi_con, con_record):  # noqa
        dbapi_con.execute('pragma foreign_keys=ON')

    with app.app_context():
        from sqlalchemy import event
        event.listen(db.engine, 'connect', _fk_pragma_on_connect)



"""
meaning of 

if __name__ == "__main__":

In Short: It Allows You to Execute Code When the File Runs as a 
Script, but Not When It’s Imported as a Module
"""


# RUNNING DEBUG MODES 
# case sensitives
# flask --app index.py --debug run

#running the app

# authentication wrappers
def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        
        req = request.json
        token = req.get('token')
        if token != '' :
            return f(*args, **kwargs)
        
        return make_response(
            'Could not verify credentials',
            401,
            {'WWW-Authenticate': 'Basic realm="Login required"'}
            )
    
    return decorated

def validate_content_type_as_json(f):
    @wraps(f)
    def decor(*args,**kwargs):
        content_type = request.headers.get('Content-Type')
        if ( content_type == 'application/json'):
            return f(*args, **kwargs)
        else:
            return make_response(
                'Content type not supported. Content must be in json format',
                401)

    return decor


# https://www.youtube.com/watch?v=J5bIPtEbS0Q&t=397s
# https://stackoverflow.com/questions/29386995/how-to-get-http-headers-in-flask
def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        # let set token to header
        token_header = request.headers.get('Authorization')
        token = token_header.split()[1]
        # to get the token you need the next item
        
        # using bearer token
        # https://stackoverflow.com/questions/63518441/how-to-read-a-bearer-token-from-postman-into-python-code
        # headers = flask.request.headers
        # bearer = headers.get('Authorization')    # Bearer YourTokenHere
        # token = bearer.split()[1]  # YourTokenHere

        if not token:
            return jsonify({'message': 'Token is missing!'}),403

        print(token)
        #checks if token is valid
        try:
            # https://pyjwt.readthedocs.io/en/latest/api.html
            # you have to specify algorithms=['thealgo']
            # https://stackoverflow.com/questions/40179995/pyjwt-returning-invalid-token-signatures
            # as indicated here
            jwt.decode(token,key=app.config['SECRET_KEY'],algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({'Message': 'Access token has expired. Please relogin'}),403
        except:
            return jsonify({'Message': 'Token is invalid!'}),403
        
        # if no wrong then return this
        return f(*args,**kwargs)

    # return the inner function to the outer function know what 
    # to do
    return decorated


# read this example of auth from website
# https://flask.palletsprojects.com/en/2.2.x/patterns/viewdecorators/
# def login_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if g.user is None:
#             return redirect(url_for('login', next=request.url))
#         return f(*args, **kwargs)
#     return decorated_function


# IMPORTANT REMINDERS #


# to run app
# flask --app index.py --debug run

#DO THIS AFTER CHANGES IN THE MODLES APP

# 1. if it says database not updated execute , else proceed to 2
#    flask db stamp head

# 2. create migrations after changing the models
#    flask db migrate

# 3. to reflect changes in the database run code below
#    flask db upgrade
