from datetime import timedelta
from flask import Flask,jsonify, render_template,session,request,make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from flask import render_template,jsonify,send_file
import smtplib
from celery import Celery
import random
from celery.schedules import crontab
import bcrypt
import redis
import pandas as pd
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager,get_jwt

from os.path import basename

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
from jinja2 import Environment, PackageLoader

ACCESS_EXPIRES = timedelta(hours=2)


application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(application)


CORS(application, origins='*')

application.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/1'


celery = Celery(application.name , broker=application.config['CELERY_BROKER_URL'])
celery.conf.update(application.config)


# Setup the Flask-JWT-Extended extension
application.config["JWT_SECRET_KEY"] = "54\x85\xfc\x1a*Y\xae"  # Change this!
application.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
jwt = JWTManager(application)

jwt_redis_blocklist = redis.StrictRedis(
    host="localhost", port=6379, db=0, decode_responses=True
)


class user(db.Model):
    __name__ = "user"
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True,nullable=False)
    uname = db.Column(db.String(80),nullable=False)
    mail = db.Column(db.String(80),nullable=False)
    password = db.Column(db.String(80),nullable=False)

class tracker(db.Model):
    __name__ = "tracker"
    u_id = db.Column(db.Integer,db.ForeignKey('user.uid'),nullable=False)
    tracker_id = db.Column(db.Integer,autoincrement=True,primary_key=True,nullable=False)
    tracker_name = db.Column(db.String(80),nullable=False)
    tracker_description = db.Column(db.String(100))
    tracker_type = db.Column(db.String(40),nullable=False)
    tracker_settings = db.Column(db.String(40))
    date_created = db.Column(db.DateTime,nullable=False, default = datetime.utcnow())

class logtable(db.Model):
    log_id = db.Column(db.Integer,primary_key=True,nullable=False,autoincrement=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.uid'),nullable=False)
    t_id = db.Column(db.Integer,db.ForeignKey('tracker.tracker_id'),nullable=False)
    Timestamp = db.Column(db.DateTime,nullable=False, default = datetime.utcnow())
    value = db.Column(db.Text,nullable=False)
    Note = db.Column(db.String(80))    

@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = jwt_redis_blocklist.get(jti)
    return token_in_redis is not None

@application.route('/')
@jwt_required()
def home():
    if not get_jwt_identity():
        raise("Identity not verified")
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@application.route("/login",methods=['GET','POST'])

def login():    
  data = request.json
  print(data['mail'],data['password'])
  encoded_pass = data['password'].encode('utf-8')
  dbdata = user.query.filter_by(mail=data['mail']).first()
  token = create_access_token(identity={"mail":dbdata.mail})
  if(bcrypt.checkpw(encoded_pass,dbdata.password)):
    return jsonify({'access_token': token, 'name':dbdata.uname,'id':dbdata.uid})
  else:
    return "Failure",402
  
@application.route('/register', methods=['GET','POST'])

def register():
    if request.method=='POST':
        data = request.json
        name = data['name']
        mail = data['mail']
        password = data['password']
        pw_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cell = user(uname=name,mail=mail,password=pw_hash)
        db.session.add(cell)
        db.session.commit()
        return "Success",200

@application.route("/logout", methods=["DELETE"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES)
    return jsonify(msg="Access token revoked")

@application.route('/forgotpass1', methods=['GET', 'POST'])
def forgotpass1():

    data = request.json
    mail = data['mail']
    print(user.query.filter_by(mail=mail).first() == None)
    if(user.query.filter_by(mail=mail).first() != None):

        otp = random.randint(1000,9999)
        file = open('otp.txt','w')
        file.write(str(otp))
        file.close
        msg = MIMEMultipart()
        msg["From"] = 'quantified.self.v2@gmail.com'
        msg["To"] = mail
        msg["Subject"] = "Reset Password(Quantified self v2)"
        body = MIMEText("Use this otp to reset your password " + str(otp))
        msg.attach(body)

        with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(user='quantified.self.v2@gmail.com', password='adlujgtvigksrqzy')
                connection.send_message(
                    msg=msg,
                    from_addr='quantified.self.v2@gmail.com',
                    to_addrs=[mail],
                )
        return jsonify({'msg' : 'Email verification sent'},{'status' : '200'})
    else:
        return jsonify({'msg':'email id does not exist'},{'status' : '666'})


            
@application.route('/verifypass', methods=['GET', 'POST'])
def verifypass():
    file = open('otp.txt','r')
    data = request.json
    otp = data['otp'] 
    for i in file:
        if(str(i)==str(otp)):
            return jsonify({'msg' : 'Email Verified'},{'status' : '200'})
        else:
            return jsonify({'msg' : 'OTP incorrect'},{'status' : '666'})

@application.route('/changepass', methods=['GET', 'POST'])
def changepass():
    data = request.json
    mail = data['mail']
    passw = data['pass']
    u = user.query.filter_by(mail=mail).first()
    pw_hash = bcrypt.hashpw(passw.encode('utf-8'), bcrypt.gensalt())
    u.password = pw_hash
    db.session.add(u)
    db.session.commit()
    return jsonify({'msg' : 'Password Successfully changed'},{'status' : '200'})


    

@application.route('/trackers/<int:id>', methods=['GET', 'POST'])
@jwt_required()
def u_tracker(id):
    table = tracker.query.filter_by(u_id=id).all()
    l = []
    for i in table:
        d = {
            'userid' : i.u_id,
            'trackerid' : i.tracker_id,
            'trackername' : i.tracker_name,
            'trackerdesc' : i.tracker_description,
            'trackertype' : i.tracker_type,
            'tracker_settings' : i.tracker_settings,
            'datecreated' : i.date_created
        }
        l.append(d)
    return jsonify(
        {
            'tracker' : l,
            'message' : 'Success'
        }
    )

@application.route('/export/<int:id>', methods=['GET', 'POST'])

def export_tracker(id):
    trackers = tracker.query.filter_by(u_id=id)
    exportable = []
    for i in trackers:
        l=[]
        l.append(i.tracker_name)
        l.append(i.tracker_description)
        l.append(i.tracker_type)
        l.append(i.tracker_settings)
        l.append(i.date_created)

        exportable.append(l)
    
    tracked = pd.DataFrame(exportable, columns=['Tracker Name','Tracker Description','Tracker Type','Tracker Settings','Date Created'])
    tracked.to_csv('your_trackers.csv',index=False)
    return send_file('your_trackers.csv')
@application.route('/trackers/delete/<int:id>', methods=['GET'])
def delete_tracker(id):
    data = tracker.query.filter_by(tracker_id=id).first()
    deletable1 = logtable.query.filter_by(t_id=id).all()
    for i in deletable1:
        db.session.delete(i)
    db.session.delete(data)
    db.session.commit()
    return jsonify({'message': 'success'})

@application.route('/trackers/update/<int:id>', methods=['GET','POST'])
def update_tracker(id):
    data = tracker.query.filter_by(tracker_id=id).first()
    if(request.method=='POST'):
        data2 = request.json
        tname = data2['tname']
        ttype = data2['ttype']
        tdesc = data2['tdesc']
        tsettings = data2['tsettings']
        data.tracker_name = tname
        data.tracker_type = ttype
        data.tracker_description = tdesc
        data.tracker_settings = tsettings
        db.session.add(data)
        db.session.commit()
    return jsonify( { 'message' : 'Success' } )


@application.route('/createtracker/<int:id>', methods=['GET', 'POST'])
def createtracker(id):
    if request.method=='POST':
        data = request.json
        tname = data['tname']
        ttype = data['ttype']
        tdesc = data['tdesc']
        tsettings = data['tsettings']
        cell = tracker(u_id=id,tracker_name=tname,tracker_type=ttype,tracker_description=tdesc,tracker_settings=tsettings)
        db.session.add(cell)
        db.session.commit()
        return "Success",200

@application.route('/addLog/<int:uid>/<int:tid>', methods=['GET', 'POST'])
def log(uid,tid):
    cell = tracker.query.filter_by(u_id=uid,tracker_id=tid).first()
    l = cell.tracker_settings.split(',')
    d = {
            'userid' : cell.u_id,
            'trackerid' : cell.tracker_id,
            'trackername' : cell.tracker_name,
            'trackerdesc' : cell.tracker_description,
            'trackertype' : cell.tracker_type,
            'tracker_settings' : cell.tracker_settings,
            'datecreated' : cell.date_created
        }

    if request.method=='POST':
        data = request.json
        val = data['value']
        note = data['note']
        
        cell = logtable(user_id=uid,t_id=tid,Note=note,value=val)
        db.session.add(cell)
        db.session.commit()

        return jsonify({'message':'success'})

    else:
        return jsonify({'data':d},{'tracker_settings' : l })

@application.route('/trackerinfo/<int:uid>/<int:tid>', methods=['GET', 'POST'])
def trackerinfo(uid,tid):
    cell = tracker.query.filter_by(u_id=uid,tracker_id=tid).first()
    logs = logtable.query.filter_by(user_id=uid,t_id=tid).all()
    l=[]
    for i in logs:
        d1 = {
            'logid' : i.log_id,
            'note' : i.Note,
            'Timestamp' : i.Timestamp,
            'value' : i.value
        }
        l.append(d1)
    d = {
            'userid' : cell.u_id,
            'trackerid' : cell.tracker_id,
            'trackername' : cell.tracker_name,
            'trackerdesc' : cell.tracker_description,
            'trackertype' : cell.tracker_type,
            'tracker_settings' : cell.tracker_settings,
            'datecreated' : cell.date_created
        }
    data = logtable.query.filter_by(t_id=tid).all()
    tracker_info = tracker.query.filter_by(tracker_id=tid).first()
    time =[]
    l1=[]
    d2={}
    if(len(data)!=0):
        if(tracker_info.tracker_type=='Numerical'):
            for i in data:
                l1.append(float(i.value))
                time.append(i.Timestamp)
            val = np.array(l1)
            time_1 = np.array(time)
            plt.plot(val) 
            plt.title('Progress')
            plt.xlabel(tracker_info.tracker_name)
            plt.ylabel('Value')
            plt.savefig('static/plot.png',dpi=300)
            plt.close()

        else:
            for i in data:                
                if(str(i.value) not in d2.keys()):
                    d2[str(i.value)] = 1
                else:
                    d2[str(i.value)]+=1
            plt.bar(list(d2.keys()), d2.values(), color='b')   
            plt.title('Progress')
            plt.xlabel(tracker_info.tracker_name)
            plt.ylabel('Value')
            plt.savefig('static/plot.png',dpi=300)
            plt.close()   
    return jsonify({'tracker_info' : d},{'logdata' : l})

@application.route('/deleteLog/<int:lid>')
def deleteLog(lid):
    deletable = logtable.query.filter_by(log_id=lid).first()
    db.session.delete(deletable)
    db.session.commit()
    return jsonify({'message' : 'success'})

#UpdateLog
@application.route('/updateLog/<int:lid>/<int:tid>',methods=['GET','POST'])
def updateLog(lid,tid):
    data = logtable.query.filter_by(log_id=lid,t_id=tid).first()
    tinfo = tracker.query.filter_by(tracker_id=tid).first()
    tsettings = tinfo.tracker_settings.split(',')

    if request.method=='POST':
        ts = datetime.utcnow()
        new = request.json
        data.Note = new['note']
        data.value = new['value']
        data.Timestamp = ts
        db.session.add(data)
        db.session.commit()
    
    d1 = {
            'logid' : data.log_id,
            'note' : data.Note,
            'Timestamp' : data.Timestamp,
            'value' : data.value
        }
        
    d = {
            'trackertype' : tinfo.tracker_type,
            'tracker_settings' : tsettings

        }
    print(d,d1)
    
    return jsonify({'tracker_info' : d},{'logdata' : d1})


@celery.task()
def monthly_report():
    with application.app_context():
        file_loader = PackageLoader("application", "templates")
        env = Environment(loader=file_loader)
        # Extracting user
        users = user.query.all()



        for ak in users:
            uid = ak.uid
            udata = ak.query.filter_by(uid=uid).first()
            trackers = tracker.query.filter_by(u_id=uid).all()
            l=[]
            for i in trackers:
                data={}

                logs = logtable.query.filter_by(t_id=i.tracker_id).all()
                if(i.tracker_type == 'Numerical' ):
                    sum,cnt = 0,0
                    for j in logs:
                        sum+=int(j.value)
                        cnt+=1
                    res = sum/cnt
                    data['tracker_name'] = i.tracker_name
                    data['res'] = res
                    l.append(data)
                else:
                    d,highest,res = {},0,''
                    for j in logs:
                        if (str(j.value) in d.keys()):
                            d[j.value]+=1
                        else:
                            d[j.value]=1
                    for j,k in d.items():
                        if(k>highest):
                            highest = k
                            res = j
                    data['tracker_name'] = i.tracker_name
                    data['res'] = res

                    l.append(data)
                
            print(l)
            
            # Creating Monthly Report in Html
            rendered = env.get_template("report.html").render(udata=udata,data=l)
            filename = "report.html"
            with open(f"{filename}", "w") as f:
                    f.write(rendered)

            msg = MIMEMultipart()
            msg["From"] = 'quantified.self.v2@gmail.com'
            msg["To"] = ak.mail
            msg["Subject"] = "Monthly Report"
            body = MIMEText("Here is your Monthly Report", "plain")
            msg.attach(body)
            with open(f"{filename}", "r") as f:
                    attachment = MIMEApplication(f.read(), Name=basename(filename))
                    attachment["Content-Disposition"] = 'attachment; filename="{}"'.format(basename(filename))

            msg.attach(attachment)

            with smtplib.SMTP("smtp.gmail.com") as connection:
                    connection.starttls()
                    connection.login(user='quantified.self.v2@gmail.com', password='adlujgtvigksrqzy')
                    connection.send_message(
                        msg=msg,
                        from_addr='quantified.self.v2@gmail.com',
                        to_addrs=[ak.mail],
                    ) 

        return "Monthly Report Sent"

@celery.task()
def daily_alert():

    users = user.query.all()

    for ak in users:
        msg = MIMEMultipart()
        msg["From"] = 'quantified.self.v2@gmail.com'
        msg["To"] = ak.mail
        msg["Subject"] = "Daily Alert"
        body = MIMEText("This is a daily reminder for you to log into your trackers")
        msg.attach(body)

        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user='quantified.self.v2@gmail.com', password='adlujgtvigksrqzy')
            connection.send_message(
                msg=msg,
                from_addr='quantified.self.v2@gmail.com',
                to_addrs=[ak.mail],
            )

            
    
    return "Daily alert sent"


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour=10, minute=0), daily_alert.s(), name='Daily Alert')
    sender.add_periodic_task(crontab(hour=11, minute=0, day_of_month=1), monthly_report.s(), name="Monthly Reports")

        

@application.route('/report')
def daily():
    monthly_report.delay()
    return jsonify({'status':'ok'})





if __name__ == "__main__":
    

    application.run(debug=True)


