from config import db
from sqlalchemy.sql import func

# additional reading especially for date time
# https://www.digitalocean.com/community/tutorials/how-to-use-flask-sqlalchemy-to-interact-with-databases-in-a-flask-application

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String,unique=True,nullable=False)
    password = db.Column(db.String,nullable=False)
    name = db.Column(db.String,nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    
    # here that backref just means that im putting a
    # new column basically into log. so im putting user 
    # on logs 
    logs = db.relationship('Log',backref="user",lazy=True)

    def __repr__(self):
        return f"""id={self.id},username={self.username}, password={self.password}, name={self.name}"""
    
class Log(db.Model):
    no = db.Column(db.Integer,primary_key=True)
    
    #note the foreign key here should be lower cased, thats 
    #mandatory. it means call the class that that you are reffering to
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    message = db.Column(db.String,nullable=False)
    # setting server default here gives the default value
    predicted_message_language = db.Column(db.String,server_default='',nullable=False)
    reply = db.Column(db.String,nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())



class DevEnvironmentTestLogs(db.Model):
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
    
