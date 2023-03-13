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

