from . import auth
from flask import render_template
from app.models import User

@auth.route('/', methods=['GET'])
def index():
    user = User.query.first()
    return render_template('index.html', user=user)
