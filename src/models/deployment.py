
from config import db
from sqlalchemy.sql import func


class UniqueTesterIdentifier(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True),server_default=func.now())
    user_agent = db.Column(db.String,default="none",nullable=True)



class UsabilityTestLogs(db.Model):
    no = db.Column(db.Integer,primary_key=True)
 
    user_message = db.Column(db.String,nullable=False)
    reply = db.Column(db.String,nullable=False)
    
    predicted_language = db.Column(db.String,nullable=False)
    # predicted_dimension_number = db.Column(db.Integer,nullable=False)
    # predicted_dimension_label = db.Column(db.String,nullable=False)
    predicted_score = db.Column(db.Numeric(3,15),default=0)

    pattern_found = db.Column(db.String,nullable=False)
    
    original_pattern_found = db.Column(db.String,default="unspecified",nullable=True)

    pattern_matching_method = db.Column(db.String,nullable=False)
    
    created_at = db.Column(db.DateTime(timezone=True),server_default=func.now())
    
    # checks if methods used are correct
    is_lang_correct = db.Column(db.Boolean,default=False,nullable=True)

    # captures information retreival response is valid or not
    is_information_retrieved_valid = db.Column(db.Boolean,default=False,nullable=True)

    #captures whether the query is within the scope or domain of influenza or diarrhea
    is_query_within_domain = db.Column(db.Boolean,default=False,nullable=True)

    test_number =  db.Column(db.Integer,default=0)

    reconstructed_message = db.Column(db.String,default="",nullable=True)
    



class UsabilityTestLogsPostgres(db.Model):
    __bind_key__ = 'postgresql'
    no = db.Column(db.Integer,primary_key=True)
 
    user_message = db.Column(db.String,nullable=False)
    reply = db.Column(db.String,nullable=False)
    
    predicted_language = db.Column(db.String,nullable=False)
    # predicted_dimension_number = db.Column(db.Integer,nullable=False)
    # predicted_dimension_label = db.Column(db.String,nullable=False)
    predicted_score = db.Column(db.Numeric(3,15),default=0)

    pattern_found = db.Column(db.String,nullable=False)
    
    original_pattern_found = db.Column(db.String,default="unspecified",nullable=True)

    pattern_matching_method = db.Column(db.String,nullable=False)
    
    created_at = db.Column(db.DateTime(timezone=True),server_default=func.now())
    
    # checks if methods used are correct
    is_lang_correct = db.Column(db.Boolean,default=False,nullable=True)

    # captures information retreival response is valid or not
    is_information_retrieved_valid = db.Column(db.Boolean,default=False,nullable=True)

    #captures whether the query is within the scope or domain of influenza or diarrhea
    is_query_within_domain = db.Column(db.Boolean,default=False,nullable=True)

    test_number =  db.Column(db.Integer,default=0)

    reconstructed_message = db.Column(db.String,default="",nullable=True)
    

