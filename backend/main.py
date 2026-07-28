'''
accs - done
schedule - helnaahhhhhhhhhhhhh
calendar -hell nahhhhhhhhhhhhhhhh
clock - done
alarms 
mail
weather api
tasks and stuff - done
talking ai
faces
'''

from flask import Flask, jsonify, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from sqlalchemy import Integer, String, LargeBinary, DateTime, ForeignKey, Column, Table, JSON, create_engine
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from flask_cors import CORS
import os, random, time

class Base(DeclarativeBase):
    pass

app = Flask(__name__)

db = SQLAlchemy(model_class=Base)

databaseURL = os.getenv('DATABASE_URL')
secretKey = os.getenv('SECRET_KEY')

app.config['SECRET_KEY'] = secretKey
app.config['SQLALCHEMY_DATABASE_URI'] = databaseURL

db.init_app(app)
CORS(app)

class user(db.Model):
    __tablename__ = "user" 
    user_id: Mapped[int] = mapped_column(Integer,  primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(200), nullable = False)
    password: Mapped[str] = mapped_column(String(200), nullable = False)
    alarms = db.relationship('alarms', backref = "user")
    todos = db.relationship('todo', backref = "user")
    timezone = db.Column(db.String(50), default='UTC', nullable=False)

#to do lists
class todo(db.Model):
    __tablename__ = "todo"
    id:Mapped[int] = mapped_column(Integer,  primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    desc: Mapped[str] = mapped_column(String(200))
    recordedTime: Mapped[datetime] = mapped_column(DateTime, default= lambda: datetime.now(timezone.utc))
    done: Mapped[bool] = mapped_column(default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

'''
#schedules - like school schedules and sum
class schedule(db.Model):
    __tablename__ = "schedule"
    id: Mapped[int] = mapped_column(Integer,  primary_key=True, autoincrement=True)
    schedule_name: Mapped[str] = mapped_column(String(200))
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
    start_time = db.Column(db.DateTime(timezone=True), nullable = True)
    end_time = db.Column(db.DateTime(timezone=True), nullable = True)
    day_id = db.Column(db.Integer, db.ForeignKey('schedule_day.id'), nullable=False)
    c
'''

class alarms(db.Model):
    __tablename__ = "alarms" 
    id: Mapped[int] = mapped_column(Integer,  primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=True)
    time = db.Column(db.Time, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable = False)
    days = db.Column(db.String(200), default = "")
    repeat: Mapped[int] = mapped_column(Integer, default=0) 
    '''
        0 - no repeat
        1 - repeat for the next day
        2 - repeat for multiple days
    '''



with app.app_context():
    db.create_all()
    


@app.route("/", methods = ["GET"])
def index():
    print("hey")
    return jsonify({'message':'Heeyy'}), 200

#USER AUTHENTICATION
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
        timezone = data.get("timezone", "UTC")
        register = user(username = usrn, password = passw, timezone = timezone)

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

#TODOS SYSTEM
@app.route("/todos", methods = ["GET", "POST"])
def todos():
    if 'user_id' in session:
        _id = session.get('user_id')
        _user = user.query.filter_by(user_id = _id).first()
        print("Yesah")
    else:
        return jsonify({
            "error":"No account found"
        }), 403

    if request.method == "POST":
        data = request.get_json()
        print(data)
        _title = data["title"]
        _desc = data.get("desc", ".")
            
        _todo = todo(title = _title, desc = _desc, user_id = _user.user_id)
        print(_todo)
        db.session.add(_todo)
        db.session.commit()
        return jsonify({
            "message": f"created todo with title {_title}"
        }), 201
    else:
        todos = db.session.scalars(db.select(todo)).all()
        _todos = []
        for t in todos:
            if t.user_id == _id:
                _todo = {
                    "title": t.title,
                    "desc": t.desc,
                    "time": t.recordedTime,
                    "done": t.done
                }   

                _todos.append(_todo)
        return jsonify(_todos), 200

@app.route("/todos/<int:id>", methods = ["GET", "PATCH", "DELETE"])    
def todoid(id):
    if 'user_id' in session:
        _id = session.get('user_id')
        _user = user.query.filter_by(user_id = _id).first()
        print("Yesah")
    else:
        return jsonify({
            "error":"No account found"
        }), 404
    
    _todo = todo.query.filter_by(id = id).first()
    if _todo is None:
        return jsonify({
            "error":"could not find todo"            
        }), 404
    
    if request.method == "PATCH":
        data = request.get_json()
        if data.get("title") is not None:
            _todo.title = data.get("title")
        if data.get("desc") is not None:
            _todo.desc = data.get("desc")
        if data.get("done") is not None:
            _todo.done = not _todo.done
            
        db.session.commit()
        return jsonify({
            "message":"succesfully edited todo"
        }), 200

    elif request.method == "DELETE":
        try:
            db.session.delete(_todo)
            db.session.commit()
            return jsonify({
                "message":"succesfully deleted todo"
            }), 200
        except:
            db.session.rollback()
            return jsonify({
                "error":"could not delete item"
            }), 500
    
    else:
        t = {
            "title": _todo.title,
            "desc": _todo.desc,
            "time": _todo.recordedTime,
            "done": _todo.done
        }
        return jsonify(t), 200

@app.route("/clock", methods = ["GET"])
def clock():

    if 'user_id' in session:
        _id = session.get('user_id')
        _user = user.query.filter_by(user_id = _id).first()
        
        time = datetime.now(ZoneInfo(_user.timezone))

        return jsonify({
            "message": str(time)
        }), 200
        
    else:
        local_time = datetime.now()
        return jsonify({
            "message": str(local_time)
        }), 200

#SCHEDULE SYSTEM -lwk abandoning it
'''
@app.route("/schedules", methods = ["GET", "POST"])
def schedules():
    if 'user_id' in session:
        _id = session.get('user_id')
        _user = user.query.filter_by(user_id = _id).first()
        print("Yesah")
    else:
        return jsonify({
            "error":"No account found"
        }), 403
    if request.method == "POST":
        #Broj dni, ime
        data = request.get_json()
        _sche_name = data.get("name", "schedule")
        _sche = schedule(schedule_name = _sche_name, user_id = _id)
        try:
            db.session.add(_sche)
            db.session.commit()
            return jsonify({
                "message": f"created schedule with the name {_sche_name}"
            }), 201
        except:
            return jsonify({
                "error":"could not create db"
            }), 400
    else:
        sches = db.session.scalars(db.select(schedule)).all()
        _sches = []
        for s in sches:
            if s.user_id == _id:
                _todo = {
                    "title": s.title,
                    "desc": s.desc,
                    "time": s.recordedTime,
                    "done": s.done
                }   

                _sches.append(_todo)
        return jsonify(_sches), 200

        
@app.route("/schedules/<int:id>", methods = ["GET", "DELETE", "PATCH"])
def schee(id):
    if 'user_id' in session:
        _id = session.get('user_id')
        _user = user.query.filter_by(user_id = _id).first()
        print("Yesah")
    else:
        return jsonify({
            "error":"No account found"
        }), 403
    _schedule = schedule.query.filter_by(id = id).first()
    if _schedule is None:
        return jsonify({
            "error":"Could not find specified schedule"
        }), 404
    
    if request.method == "DELETE":
        try:
            db.session.delete(_schedule)
            db.session.commit()
            return jsonify({
                "message":"succesfully deleted todo"
            }), 200
        except:
            db.session.rollback()
            return jsonify({
                "error":"could not delete item"
            }), 500
    
    elif request.method == "PATCH":
        try:
            data = request.get_json()
            _name = data.get("name", "")
            _schedule.schedule_name = _name
            return jsonify({
                "message":"Managed to change name"
            }), 200
        except:
            return jsonify({"error":"could not patch item"}), 500

    else:
        return jsonify({
            "name": _schedule.schedule_name,
            #add days and their events
        })


@app.route("/schedules/<int:schedule_id>/<int:day_id>", methods = ["GET", "POST", "DELETE", "PUT"])
def scheday(sid, did):
    if 'user_id' in session:
        _id = session.get('user_id')
        _user = user.query.filter_by(user_id = _id).first()
        print("Yesah")
    else:
        return jsonify({
            "error":"No account found"
        }), 403

    _schedule = schedule.query.filter_by(id = sid).first()
    if _schedule is None:
        return jsonify({
            "error":"Could not find specified schedule"
        }), 404

    _day = schedule_day.query.filter_by(id = did).first()
    if _day is None and request.method != "POST":
        return jsonify({
            "error":"Could not find specified day"
        }), 404

    if request.method == "POST":
        data = request.get_json()
        _day_of_week = data.get("day", "0")
        if _day_of_week == 0:
            return jsonify({
                "error":"day of the week does not exist, pick a number between 1 and 7"
            }), 400

        d = schedule_day(day_of_week = _day_of_week, schedule_id = sid)
        try:
            db.session.add(d)
            db.session.commit(d)
            return jsonify({
                "error":"Operation success"
            })
        except:
            return jsonify({
                "error":"db management problem"
            }), 500
    elif request.method == "PUT":
        try:
            data = request.get_json()
            _new_day = data.get("day", _day.day_of_the_week)
            _day.day_of_the_week = _new_day
            db.session.commit()
            return jsonify({
                "message":"Successfully edited"
            }), 200
        
        except:
            return jsonify({
                "error":"Couldnt edit day"
            }), 500
    elif request.method == "DELETE":
        try:
            db.session.delete(_day)
            db.session.commit()
            return jsonify({
                "message":"succesfully deleted todo"
            }), 200
        except:
            db.session.rollback()
            return jsonify({
                "error":"could not delete item"
            }), 500
    



@app.route("/schedules/<int:schedule_id>/<int:day_id>/<int:event_id>")
def schedayev(sid, did, evid):
    if 'user_id' in session:
        _id = session.get('user_id')
        _user = user.query.filter_by(user_id = _id).first()
        print("Yesah")
    else:
        return jsonify({
            "error":"No account found"
        }), 403

    _schedule = schedule.query.filter_by(id = sid).first()
    if _schedule is None:
        return jsonify({
            "error":"Could not find specified schedule"
        }), 404


    _day = schedule_day.query.filter_by(id = did).first()
    if _day is None:
        return jsonify({
             "error":"Could not find specified day"
        }), 404
    
    
    _ev = event_sch.query.filter_by(id = did).first()
    if _ev is None and request.method != "POST":
        return jsonify({
             "error":"Could not find specified event"
        }), 404


    if request.method == "POST":
        data = request.get_json()
        _title = data.get("title", None)
        if _title is None:
            return jsonify({
                "error":"required title"
            }), 400

        _desc = data.get("desc", "")

        ad = data.get("all_day", False)
        if ad != False:
            ad = True

        try:
            start_dt = datetime.fromisoformat(data['start_time']).astimezone(timezone.utc)
            end_dt = datetime.fromisoformat(data['end_time']).astimezone(timezone.utc)
        except:
            ad = True
            start_dt = None
            end_dt = None


        e = event_sch(name = _title, desc = _desc, all_day = ad, start_time = start_dt, end_time = end_dt, day_id = did)
        try:
            db.session.add(e)
            db.session.commit(e)
            return jsonify({
                "error":"Operation success"
            })
        except:
            return jsonify({
                "error":"db management problem"
            }), 500

        
    elif request.method == "PUT":
        try:
            data = request.get_json()
            _title = data.get("title", _ev.name)
            _ev.name = _title

            _desc = data.get("desc", _ev.desc)
            _ev.desc = _desc
            if 'start_time' in data:
                try:
                    start_dt = datetime.fromisoformat(data['start_time']).astimezone(timezone.utc)
                except ValueError:
                    return jsonify({'error': 'Invalid start_time format.'}), 400
                _ev.start_time = start_dt
            if 'end_time' in data:
                try:
                    end_dt = datetime.fromisoformat(data['end_time']).astimezone(timezone.utc)
                except ValueError:
                    return jsonify({'error': 'Invalid end_time format.'}), 400
                _ev.end_time = end_dt
            if end_dt <= start_dt:
                return jsonify({'error': 'End time must be after start time.'}), 400

                
            db.session.commit()
            return jsonify({
                "message":"Successfully edited"
            }), 200
        
        except:
            return jsonify({
                "error":"Couldnt edit the event"
            }), 500


        
    elif request.method == "DELETE":
        try:
            db.session.delete(_ev)
            db.session.commit()
            return jsonify({
                "message":"succesfully deleted todo"
            }), 200
        except:
            db.session.rollback()
            return jsonify({
                "error":"could not delete item"
            }), 500
        
    
    '''

@app.route("/alarms", methods = ["GET", "POST"])
def alarm():
    if 'user_id' in session:
        _id = session.get('user_id')
        _user = user.query.filter_by(user_id = _id).first()
        print("Yesah")
    else:
        return jsonify({
            "error":"No account found"
        }), 403

    if request.method == "POST":
        data = request.get_json()

        days = data.get("days", "")
        if days == "":
            _repeat = data.get("repeat", 0)
        else:
            _repeat = 2
        time = data.get("time", None)
        if time is None:
            print("no")
            return jsonify({"error":"time is required"}), 400
        title = data.get("title", "")
        _time = datetime.strptime(time, "%H:%M").time()

        alarm = alarms(
            title = title,
            user_id = _id,
            time = _time,
            days = days,
            repeat = _repeat
        )

        db.session.add(alarm)
        db.session.commit()
        return jsonify({
            "message":"successfully created"
        }), 201

    __alarms = db.session.scalars(db.select(alarms)).all()
    _alarms = []
    for t in __alarms:
        if t.user_id == _id:

            _todo = {
                "title": t.title,
                "time": str(t.time),
                "days": t.days
            }   

            _alarms.append(_todo)
    return jsonify(_alarms), 200

    
    

@app.route("/alarms/<int:id>", methods = ["GET", "PATCH", "DELETE"])
def alarmed(id):
    if 'user_id' in session:
        _id = session.get('user_id')
        _user = user.query.filter_by(user_id = _id).first()
        print("Yesah")
    else:
        return jsonify({
            "error":"No account found"
        }), 403

    a = alarms.query.filter_by(id = id).first()
    if a is None:
        return jsonify({
            "error":"could not find todo"            
        }), 404
    
    if request.method == "PATCH":
        data = request.get_json()
        if data.get("title") is not None:
            a.title = data.get("title", a.title)
        if data.get("time") is not None:
            a.time = datetime.strptime(data.get("time"), "%H:%M").time()
        if data.get("days") is not None:
            a.days = data.get("days")
        if data.get("repeat") is not None:
            a.repeat = data.get("repeat")
                    
        db.session.commit()
        return jsonify({
            "message":"succesfully edited todo"
        }), 200

    elif request.method == "DELETE":
        try:
            db.session.delete(a)
            db.session.commit()
            return jsonify({
                "message":"succesfully deleted todo"
            }), 200
        except:
            db.session.rollback()
            return jsonify({
                "error":"could not delete item"
            }), 500
    
    else:
        t = {
            "title": a.title,
            "time": str(a.time),
            "days": a.days,
            "repeat": a.repeat
        }
        return jsonify(t), 200
    


    