from flask import Flask, request,jsonify,render_template, redirect,url_for
from config import app, auth_required,validate_content_type_as_json
from models.models import *
from sqlalchemy.exc import IntegrityError,NoForeignKeysError

# https://www.youtube.com/watch?v=pjVhrIJFUEs

from routes.user import user
from routes.log import log
from routes.test import test
from routes.usability import usability
from routes.classifier import classifier

app.register_blueprint(user)
app.register_blueprint(log)
app.register_blueprint(test)
app.register_blueprint(classifier)
app.register_blueprint(usability)


@app.route("/")
def hello_world():
    # flask automatically find template in template folders
    # return render_template('/index.jinja')
    return redirect(url_for('usability.site.show_unique_tester_id'))

@app.route("/unprotected",endpoint="show_unprotected_page")
def unprotected():
    return render_template('./views/_unprotected.jinja')


# so order do matter
@app.route("/protected",endpoint="show_protected_page")
@validate_content_type_as_json
@auth_required
def unprotected():
    return render_template('./views/_protected.jinja')
