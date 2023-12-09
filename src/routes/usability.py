from flask import request, Blueprint, render_template,jsonify,redirect,url_for
from config import db, app,validate_content_type_as_json,token_required
from models.deployment import UsabilityTestLogs,UniqueTesterIdentifier
from sqlalchemy.exc import IntegrityError,NoForeignKeysError
from sqlalchemy import func

# export log 
usability = Blueprint('usability',__name__,url_prefix="/usability")

# sub blueprint
api = Blueprint('api',__name__,url_prefix="/api")
site = Blueprint('site',__name__,url_prefix="/site")

# connect sub blue plints to main
usability.register_blueprint(api)
usability.register_blueprint(site)

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

@site.route('/show_unique_tester_id',methods=['GET'],endpoint="show_unique_tester_id")
def show_unique_tester_id():
    uniqueIdentifiers = db.paginate(
                db.select(UniqueTesterIdentifier)
                .order_by(UniqueTesterIdentifier.created_at.desc()),
                per_page=10)
    return render_template('views/usability/show_unique_testers.jinja', records=uniqueIdentifiers)


@api.route("/store", methods=['POST'])
def store_test_data():
    req = request.json
    
    # https://thispointer.com/how-to-iterate-over-a-json-object-in-python/
    # receiving ang iterating an array in json
    # print("Received Bulk Data")
    # print("Received Data Type: ",type(req))
    # print("Received data:: ", req)

    try:
            
        data = UsabilityTestLogs(
            user_message = req.get("userMessage"),
            reply = req.get("reply"),
            predicted_language = req.get("lang"),
            # predicted_dimension_number = data["dimensionCode"],
            # predicted_dimension_label = data["dimensionLabel"],
            pattern_found = req.get("pattern"),
            pattern_matching_method = req.get("patternMatchingMethod"),
            test_number = req.get("testNumber"),
            predicted_score = req.get("score"),
            reconstructed_message= req.get("reconstructedMessage"),
            original_pattern_found=req.get("originalPatternFound")
        )
        

        print(data)

        db.session.add(data)
        db.session.commit()

        print("Added Usability Test Data")
    except ValueError as e:
        db.session.rollback()
        print("An Error occured adding usability data", e)
        return jsonify(msg="Unable to add usability test data")

    return jsonify(msg="Test data has been added"),200



@site.route("/get_user_conversations/<id>",endpoint="get_user_conversations",methods=['POST','GET'])
def get_user_conversations(id):

    cases = ""
    # https://stackoverflow.com/questions/23067750/flask-sqlalchemy-max-value-of-column
        # if latest get the max // dont forget to add .scalar()
  

    # https://stackoverflow.com/questions/47841108/how-check-if-value-exists-in-request-p
    cases =  db.paginate(
                db.select(UsabilityTestLogs).filter_by(test_number=id)
                    .order_by(UsabilityTestLogs.created_at.desc()),
                        per_page=50)
        
        
        
        # To count counting total read below 
        # https://stackoverflow.com/questions/34692571/how-to-use-count-in-flask-sqlalchemy
    total_correct_info = UsabilityTestLogs.query.filter_by(
            is_information_retrieved_valid=1,
            # is_query_within_domain=1,
            test_number=id).count()
   
    
    total_incorrect_info = UsabilityTestLogs.query.filter_by(
        is_information_retrieved_valid=0,
        test_number=id).count()
        
    return render_template('views/usability/get_user_conversations.jinja',
                           testLogs=cases,
                           test_id=id,
                           total_correct_info=total_correct_info,
                           total_incorrect_info=total_incorrect_info)

# @site.route("/retrieved/invalid",endpoint="show_invalid_test_cases",methods=['POST','GET'])
# def show_test_cases():
#     # items = DevEnvironmentTestLogs.query.all()
#     # get max number
#     test_id = db.session.query(func.max(UsabilityTestLogs.test_number)).scalar()
#     if request.method == 'GET':
#         cases =  db.paginate(
#                     db.select(UsabilityTestLogs)
#                         .filter_by(test_number=test_id,is_information_retrieved_valid=0)
#                         .order_by(UsabilityTestLogs.created_at.desc()),
#                         per_page=200)
#     elif request.method == 'POST':
#         test_id = request.form.get('test_id')
#         cases =  db.paginate(
#                     db.select(UsabilityTestLogs)
#                         .filter_by(test_number=test_id,is_information_retrieved_valid=0)
#                         .order_by(UsabilityTestLogs.created_at.desc()),
#                         per_page=200)
#     return render_template('views/test_errors.jinja',testLogs=cases,test_id=test_id)

@api.route("/update/lang_status",methods=['POST'],endpoint="update_language_status")
def update_lang_status():
    req = request.json
    id = req["id"]
    status = req['status']
    target = UsabilityTestLogs.query.filter_by(no=id).first()

    if status == "False":
        status = False
    else:
        status = True   
 
    target.is_lang_correct = bool(status)

    print(f"Update lang:: {id}/{status}")

    try:
        # this all you need
        db.session.commit()
        return "Updated Language To Correct"
    except Exception as e:
        print('Error occured in updating language: ', e)
        db.session.rollback()
        return "Something went wrong. Update was not performed"


@api.route("/update/query_within_domain_status",methods=['POST'],endpoint="query_within_domain_status")
def update_query_status():
    req = request.json
    id = req["id"]
    status = req['status']
    target = UsabilityTestLogs.query.filter_by(no=id).first()

    if status == "False":
        status = False
    else:
        status = True
 
    target.is_query_within_domain = bool(status)

    try:
        # this all you need
        db.session.commit()
        return "Updated Language To Correct"
    except:
        db.session.rollback()
        return "Something went wrong. Update was not performed"



@api.route("/update/information_retreived_status",methods=['POST'],endpoint="information_retreived_status")
def update_reply_status():
    req = request.json
    id = req["id"]
    status = req['status']
    target = UsabilityTestLogs.query.filter_by(no=id).first()

    if status == "False":
        status = 0
    else:
        status = 1    
 
    target.is_information_retrieved_valid = bool(status)

    try:
        # this all you need
        db.session.commit()
        return "Updated Language To Correct"
    except:
        db.session.rollback()
        return "Something went wrong. Update was not performed"
    
