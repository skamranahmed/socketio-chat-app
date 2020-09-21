from time import strftime, localtime

from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_socketio import SocketIO, send, emit, join_room, leave_room

from wtform_fields import RegistrationForm, LoginForm
from passlib.hash import pbkdf2_sha256

from models import SQLAlchemy, User

app = Flask(__name__)
app.secret_key = 'this has to be changed later'

#  Configure DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://vtixpkmljdimhi:8c81a851f7261ad1ac0e71a5fa82cecb6b3dd79ef4cf64d59aa9c' \
                                       '4434c22c17a@ec2-3-218-75-21.compute-1.amazonaws.com:5432/d52cq48f8e1dnq'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app = app)

#  Initializing Flask Socket-IO
socketio = SocketIO(app = app)
ROOMS = ['Python', 'C++', 'Javascript']

#  Configure flask login
login = LoginManager(app = app)
login.init_app(app = app)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


# noinspection PyArgumentList
@app.route('/', methods = ['GET', 'POST'])
def index():

    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data

        hashed_pwd = pbkdf2_sha256.hash(password)

        #  Added a custom validator for username in wtform_fields.py, therefore no need for this check here
        # #  Check if username already exists
        # user_object = User.query.filter_by(username = username).first()
        # if user_object:
        #     return "Someone else has taken this username"

        #  Add user to DB
        user = User(username=username, password=hashed_pwd)
        db.session.add(user)
        db.session.commit()

        flash('Registered successfully. Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('index.html', form = reg_form)


@app.route("/login/", methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('chat'))

    login_form = LoginForm()

    #  Allow login if validation success
    if login_form.validate_on_submit():
        user_object = User.query.filter_by(username = login_form.username.data).first()
        login_user(user = user_object)
        return redirect(url_for('chat'))

    return render_template('login.html', form = login_form)


@app.route("/chat/", methods = ['GET', 'POST'])
# @login_required
def chat():

    # if not current_user.is_authenticated:
    #     flash('Please login, before accessing chat', 'danger')
    #     return redirect(url_for('login'))

    return render_template('chat.html', username = current_user.username, rooms = ROOMS)


@app.route("/logout/", methods = ['GET'])
def logout():

    if not current_user.is_authenticated:
        flash('You are not logged in!', 'danger')
        return redirect(url_for('login'))

    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))

#  client will send message to this event bucket on the server
@socketio.on('message')
def message(data):
    # print("="*40)
    print(f"{data}")
    # print("="*40)

    #  send will broadcast the message received by the server, to all the connected clients on the message bucket
    # send(data)
    send({'msg': data['msg'], 'username': data['username'], 'time_stamp': strftime('%b-%d %I:%M%p', localtime())})

    #  this will broadcast the message to an event bucket named custom
    # emit('custom', 'This is a custom message')


@socketio.on('join')
def join(data):

    join_room(data['room'])
    send({'msg': f"{data['username']} has joined the {data['room']} room"}, room = data['room'])

@socketio.on('leave')
def leave(data):

    leave_room(data['room'])
    send({'msg': f"{data['username']} has left the {data['room']} room"}, room = data['room'])

if __name__ == '__main__':
    # app.run(debug = True)
    socketio.run(app = app, debug = True)