from flask import request, Blueprint, render_template,jsonify,redirect,url_for
from config import db, app,validate_content_type_as_json,token_required
from models.models import Log,User,DevEnvironmentTestLogs
from sqlalchemy.exc import IntegrityError,NoForeignKeysError
from sqlalchemy import func

# export log 
test = Blueprint('test',__name__,url_prefix="/test")

# sub blueprint
api = Blueprint('api',__name__,url_prefix="/api")
site = Blueprint('site',__name__)

# connect sub blue plints to main
test.register_blueprint(api)
test.register_blueprint(site)


@site.route("/",endpoint="show_test_cases",methods=['POST','GET'])
def show_test_cases():
    # items = DevEnvironmentTestLogs.query.all()
    cases = ""
    # https://stackoverflow.com/questions/23067750/flask-sqlalchemy-max-value-of-column
        # if latest get the max // dont forget to add .scalar()
    test_id = db.session.query(func.max(DevEnvironmentTestLogs.test_number)).scalar()
    
    if request.method == 'GET':
        # https://stackoverflow.com/questions/47841108/how-check-if-value-exists-in-request-p
        cases =  db.paginate(
                db.select(DevEnvironmentTestLogs).filter_by(test_number=test_id).order_by(DevEnvironmentTestLogs.created_at.desc()),
                per_page=50)
        
    elif request.method == 'POST':
        # get max valueost
        test_id = request.form.get("test_id")
        cases =  db.paginate(
                db.select(DevEnvironmentTestLogs).filter_by(test_number=test_id).order_by(DevEnvironmentTestLogs.created_at.desc()),
                per_page=50)
        
        
        # To count counting total read below 
        # https://stackoverflow.com/questions/34692571/how-to-use-count-in-flask-sqlalchemy
    total_correct_info = DevEnvironmentTestLogs.query.filter_by(
            is_information_retrieved_valid=1,
            # is_query_within_domain=1,
            test_number=test_id).count()
   
    
    total_incorrect_info = DevEnvironmentTestLogs.query.filter_by(
        is_information_retrieved_valid=0,
        test_number=test_id).count()
        
    return render_template('views/test.jinja',
                           testLogs=cases,
                           test_id=test_id,
                           total_correct_info=total_correct_info,
                           total_incorrect_info=total_incorrect_info)

@site.route("/retrieved/invalid",endpoint="show_invalid_test_cases",methods=['POST','GET'])
def show_test_cases():
    # items = DevEnvironmentTestLogs.query.all()
    # get max number
    test_id = db.session.query(func.max(DevEnvironmentTestLogs.test_number)).scalar()
    if request.method == 'GET':
        cases =  db.paginate(
                    db.select(DevEnvironmentTestLogs)
                        .filter_by(test_number=test_id,is_information_retrieved_valid=0)
                        .order_by(DevEnvironmentTestLogs.created_at.desc()),
                        per_page=200)
    elif request.method == 'POST':
        test_id = request.form.get('test_id')
        cases =  db.paginate(
                    db.select(DevEnvironmentTestLogs)
                        .filter_by(test_number=test_id,is_information_retrieved_valid=0)
                        .order_by(DevEnvironmentTestLogs.created_at.desc()),
                        per_page=200)
    return render_template('views/test_errors.jinja',testLogs=cases,test_id=test_id)

@api.route("/update/lang_status",methods=['POST'],endpoint="update_language_status")
def update_lang_status():
    req = request.json
    id = req["id"]
    status = req['status']
    target = DevEnvironmentTestLogs.query.filter_by(no=id).first()

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
    target = DevEnvironmentTestLogs.query.filter_by(no=id).first()

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
    target = DevEnvironmentTestLogs.query.filter_by(no=id).first()

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
    


# @api.route("/store", methods=['POST'])
# def store_test_data():
#     data = request.json
    
#     # https://thispointer.com/how-to-iterate-over-a-json-object-in-python/
#     # receiving ang iterating an array in json
#     print("Received Bulk Data")

#     try:

#         test = DevEnvironmentTestLogs(
#             user_message=data["userMessage"],
#             reply=data["reply"],
#             predicted_language=data["lang"],
#             predicted_dimension_number=data["dimensionCode"],
#             predicted_dimension_label=data["dimensionLabel"],
#             pattern_found=data["pattern"],
#             pattern_matching_method=data["patternMatchingMethod"]
#         )

#         db.session.add(test)
#         db.session.commit()
#     except:
#         db.session.rollback()
#         return "Something went wrong in committing test"

#     return jsonify(msg="Test data has been added")

@api.route("/store", methods=['POST'])
def store_test_data():
    req = request.json
    
    # https://thispointer.com/how-to-iterate-over-a-json-object-in-python/
    # receiving ang iterating an array in json
    print("Received Bulk Data")
    print("Received Data Type: ",type(req))
    print("Received data:: ", req)

    try:

        for data in req:

            # num = data["dimensionCode"]
            
            test = DevEnvironmentTestLogs(
                user_message = data["userMessage"],
                reply = data["reply"],
                predicted_language = data["lang"],
                # predicted_dimension_number = data["dimensionCode"],
                # predicted_dimension_label = data["dimensionLabel"],
                pattern_found = data["pattern"],
                pattern_matching_method = data["patternMatchingMethod"],
                test_number = data["testNumber"],
                predicted_score = data["score"],
                reconstructed_message= data["reconstructedMessage"],
                original_pattern_found=data["originalPatternFound"]
            )
            
            db.session.add(test)
        
        db.session.commit()

        print("Ended Bulk Data")
    except ValueError as e:
        db.session.rollback()
        print("An Error occured", e)
        return "Something went wrong in committing test"

    return jsonify(msg="Test data has been added")