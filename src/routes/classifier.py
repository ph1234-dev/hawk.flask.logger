from flask import request, Blueprint, render_template,jsonify
from config import db, model, feature_vectorizer
from models.models import Log
from sqlalchemy.exc import IntegrityError,NoForeignKeysError


#classifier 
classifier = Blueprint('classifier',__name__,url_prefix="/classify")

# sub blueprint
api = Blueprint('api',__name__,url_prefix="/api")
site = Blueprint('site',__name__)

# connect sub blue plints to main
classifier.register_blueprint(api)
classifier.register_blueprint(site)



@api.route('/predict',methods=['POST'])
def classify():
    if request.is_json:
        req = request.json
        msg = req.get("message")

        msg = feature_vectorizer.transform([msg])
        
        # this returns an array containing one data ['the data']
        # so to access get the 0 index item
        lang = model.predict(msg)
        lang = lang[0]
        print(f"Predicted lang=>{lang}")
        # sample array 
        # random.randrange(20, 50, 3)

        # https://sentry.io/answers/return-json-in-flask-view/
        # return f"{lang}"
        # return jsonify(
        #     lang=lang,
        #     msg=msg
        # )
        return {
            "lang": lang
        }
    else:
        return "Received invalid json on prediction"


@site.route('/playground',endpoint="show_playground")
def playground():
    # searches on template forler 
    return render_template('/views/classification_playground.jinja')