from flask import Flask, render_template

from wtform_fields import RegistrationForm
from models import SQLAlchemy, User

app = Flask(__name__)
app.secret_key = 'this has to be changed later'

#  Configure DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://vtixpkmljdimhi:8c81a851f7261ad1ac0e71a5fa82cecb6b3dd79ef4cf64d59aa9c' \
                                       '4434c22c17a@ec2-3-218-75-21.compute-1.amazonaws.com:5432/d52cq48f8e1dnq'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app = app)

@app.route('/', methods = ['GET', 'POST'])
def index():

    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data

        #  Check if username already exists
        user_object = User.query.filter_by(username = username).first()
        if user_object:
            return "Someone else has taken this username"

        #  Add user to DB
        user = User(username = username, password = password)
        db.session.add(user)
        db.session.commit()
        return "User Added to DB"

    return render_template('index.html', form = reg_form)


if __name__ == '__main__':
    app.run(debug = True)
