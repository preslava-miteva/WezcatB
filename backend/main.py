'''
accs
schedule
clock
alarms
weather api
calendar
tasks and stuff
talking ai
'''

from flask import Flask, jsonify, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from sqlalchemy import Integer, String, LargeBinary, DateTime, ForeignKey, Column, Table, JSON, create_engine
from datetime import datetime, timezone
from flask_cors import CORS
import os, random, time


class Base(DeclarativeBase):
    pass

app = Flask(__name__)

db = SQLAlchemy(model_class=Base)

databaseURL = os.getenv('DATABASE_URL')
secretKey = os.getenv('SECRET_KEY')
app = Flask(__name__)
app.config['SECRET_KEY'] = secretKey
app.config['SQLALCHEMY_DATABASE_URI'] = databaseURL

db.init_app(app)
CORS(app)

class user(db.Model):
    __tablename__ = "user" 
    user_id: Mapped[int] = mapped_column(Integer,  primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(200), nullable = False)
    password: Mapped[str] = mapped_column(String(200), nullable = False)
    schedules = db.relationship('schedule', backref = "user")
    todos = db.relationship('todo', backref = "user")

#to do lists
class todo(db.Model):
    __tablename__ = "todo"
    id:Mapped[int] = mapped_column(Integer,  primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    desc: Mapped[str] = mapped_column(String(200))
    recordedTime: Mapped[datetime] = mapped_column(DateTime, default= lambda: datetime.now(timezone.utc))
    done: Mapped[bool] = mapped_column(default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)


#schedules - like school schedules and sum
class schedule(db.Model):
    __tablename__ = "schedule"
    id: Mapped[int] = mapped_column(Integer,  primary_key=True, autoincrement=True)
    schedule_name: Mapped[str] = mapped_column(String(200))
    day_num: Mapped[int] = mapped_column(Integer)
    days = db.relationship('schedule_day', backref = "schedule")
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

class schedule_day(db.Model):
    __tablename__ = "schedule_day"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    day_of_the_week: Mapped[int] = mapped_column(Integer)
    events = db.relationship('event_sch', backref = "day")
    schedule_id = db.Column(db.Integer, db.ForeignKey('schedule.id'), nullable = False)

class event_sch(db.Model):
    __tablename__ = "event_sch"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200))
    desc: Mapped[str] = mapped_column(String(200), nullable=True)
    all_day: Mapped[bool] = mapped_column(default=True)
    start_time = db.Column(db.Time, nullable = True)
    end_time = db.Column(db.Time, nullable = True)
    day_id = db.Column(db.Integer, db.ForeignKey('schedule_day.id'), nullable=False)

with app.app_context():
    db.create_all()
    

@app.route("/", methods = ["GET"])
def index():
    print("hey")
    return jsonify({'message':'Heeyy'}), 200

@app.route("/logIn", methods = ['POST'])
def logIn():
    if 'user_id' in session:
            _user = user.query.get(session['user_id'])
            logOut()
            print("successful logout")
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        usrn = data['username']
        pasw = data['password']
        _user = user.query.filter_by(username=usrn).first()
        if _user is None:
            print("not asdhisio")
        if _user and check_password_hash(_user.password, pasw):
            session['user_id'] = _user.user_id
            print(_user.user_id)
            return jsonify({
                "logged in": True,
                "message": f"managed to log in as {_user.username}",
                "user_id": _user.user_id
            }), 201
        return jsonify({
            "logged in": False,
            "error": "Username or password incorrect",
        }), 401
    

@app.route("/signUp", methods = ['GET','POST'])
def signUp():
    if 'user_id' in session:
            _user = user.query.get(session['user_id'])
            logOut()
            print("successful logout")
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        usrn = data['username']
        pasw = data['password']
        existing_user = user.query.filter_by(username=usrn).first()
        if existing_user:
            return jsonify({
                "signed in": False,
                "error": "Username taken",
            }), 400
        passw = generate_password_hash(pasw)
        register = user(username = usrn, password = passw)

        db.session.add(register)
        db.session.commit()
        print(register.username)
        print(register.user_id)

        return jsonify({
            "Signed up": True,
            "message": f"Signed up as {usrn}"
        }), 201
    

@app.route("/logOut", methods = ["DELETE"])
def logOut():
    session.pop('user_id', None)
    return jsonify({
        "message": "logged out"
    }), 200
