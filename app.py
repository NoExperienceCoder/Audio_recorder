import webbrowser
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#import datetime
import jinja2
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///FinalBase.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
db= SQLAlchemy(app)

class MeetInfo(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    link = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(60), nullable = False)
    sched_date = db.Column(db.DateTime, nullable = False)
    date_regis = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.name} - {self.email}"
class GeneralInfo(db.Model):
    ser = db.Column(db.Integer, primary_key = True)
    uname = db.Column(db.String(50), nullable = False)
    uemail = db.Column(db.String(50), nullable = False)
    upass = db.Column(db.String(20), nullable = False)
    unum = db.Column(db.Integer, nullable = False)

    def __repr__(self) -> str:
        return f"{self.name} - {self.uemail}"

@app.route('/addMeet',methods=['GET','POST'])
def hello_world():
    if request.method=='POST':
        link = request.form['link']
        email = request.form['email']
        sched_date = request.form['sched_date']
        dt = datetime.strptime(sched_date,'%Y-%m-%dT%H:%M')
        inp = MeetInfo(link = link, email = email, sched_date= dt)
        db.session.add(inp)
        db.session.commit()
        
    allrec = MeetInfo.query.all()
    return render_template('input.html', allrec = allrec)
@app.route('/')
def temp():
    return render_template('main.html')

@app.route('/RegisData', methods=['GET','POST'])
def regist():
    if request.method=='POST':
        uname= request.form['Name']
        email = request.form['email']
        pass_1 = request.form['pass']
        pass_2 = request.form['repass']
        mob = request.form['phone']
        counter = GeneralInfo.query.filter_by(uemail=email).first()
        if counter is None:
         if ((pass_1==pass_2) and (len(pass_1)>=8)):
           reginp = GeneralInfo(uname = uname, uemail = email, upass = pass_1, unum = mob)
           db.session.add(reginp)
           db.session.commit()
           return render_template('input.html')
         else : 
          return render_template('error.html')
        else: 
            return render_template('login.html')    

@app.route('/update/<int:sno>',methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        link = request.form['link']
        email = request.form['email']
        sched_date = request.form['sched_date']
        info = MeetInfo.query.filter_by(sno=sno).first()
        info.link = link
        info.email = email
        info.sched_date = sched_date
        db.session.add(info)
        db.session.commit()
        return redirect('/addMeet')
    info = MeetInfo.query.filter_by(sno=sno).first()
    return render_template('update.html', info = info)

@app.route('/remove/<int:sno>')
def remove(sno):
    dellink = MeetInfo.query.filter_by(sno = sno).first()
    db.session.delete(dellink)
    db.session.commit()
    return redirect('/addMeet')

@app.route('/existUser')
def transfer():
    return render_template('login.html')

@app.route('/newUser')
def transfer1():
    return render_template('regis.html')

@app.route('/LoginAcc',methods=['GET','POST'])
def Authenticate():
    if request.method=='POST':
        temail = request.form['tuser']
        tpass1 = request.form['tpass']
        check = GeneralInfo.query.filter_by(uemail = temail).first()
        if ((check.uemail==temail) and (check.upass==tpass1)):
            return render_template('input.html')
        else : 
            return render_template('error.html')    

@app.route('/openLink/<int:sno>')
def JoinNow(sno):
    joinLink =  MeetInfo.query.filter_by(sno = sno).first()
    url = joinLink.link
    webbrowser.open_new_tab(url)
    return render_template('record.html')

@app.route('/SaveAs', methods =['GET','POST'])
def save():
    if request.method=='POST':
        save_name = request.form['SaveAs']
        return render_template('record.html', save_name)

@app.route('/SendMail', methods = ['GET','POST'])
def send_notif():
    if request.method=='POST':
     getTime = MeetInfo.query.filter(MeetInfo.sched_date).all()
     nowTime = datetime.now()
     for inp_time in getTime:
        if inp_time==nowTime:
            return render_template('new.html')
    return redirect('/addMeet')                


if __name__ =="main":
    app.run(debug = True)