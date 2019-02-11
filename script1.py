from flask import Flask, render_template, request
import pandas as pd
from send_email import send_email
import sqlite3 as sq

vcv=Flask(__name__)
@vcv.route("/")
def index():
    return render_template("index.html")

@vcv.route('/home', methods=['POST'])
def home():
    if request.method=='POST':
        df = pd.read_json("ld.json")
        email=request.form["email_name"]
        passw=request.form["pass_w"]
        if email in list(df['email']):
            a=open("current.txt",'w')
            a.seek(0)
            a.write(email)
            a.truncate()
            a.close()
            df=df.set_index('email')
            if passw == df.loc[email,'password']:
                return render_template("select1.html")
    return render_template("fail.html")
@vcv.route('/feedback', methods=['POST'])
def feedback():
    if request.method=='POST':
        df = pd.read_json("ld.json")
        df=df.set_index('email')
        a=open("current.txt",'r')
        b=a.readline()
        a.close()
        service=request.form["service_name"]
        rating=request.form["rating"]
        comments=request.form["comments"]
        improvements=request.form["improvements"]
        suggestions=request.form["suggestions"]
        try:
            name=df.loc[b,'name']
        except KeyError :
            return "Please login again"
        conn=sq.connect("data.db")
        cur=conn.cursor()
        cur.execute("INSERT INTO store VALUES(?,?,?,?,?,?)",(b,service,rating,comments,improvements,suggestions))
        conn.commit()
        conn.close()
        send_email(b,name,'egjewus',1)
        print(b,'added to database')
        return render_template("success.html")
@vcv.route('/reset')
def reset():
    return render_template("reset.html")

@vcv.route('/forget', methods=['POST'])
def forget():
    if request.method=='POST':
        df = pd.read_json("ld.json")
        email=request.form["email_name"]
        if email in list(df['email']):
            a=email
            df=df.set_index('email')
            password=df.loc[email,'password']
            name=df.loc[email,'name']
            send_email(email,name,password,0)
            return render_template("forget.html")
    return render_template("fail.html")

@vcv.route('/about/')
def about():
    return render_template("about.html")
@vcv.route('/fail/')
def fail():
    return render_template("fail.html")
@vcv.route('/home1')
def home1():
    return render_template("home.html")
@vcv.route('/quizes/')
def quizes():
    return render_template("quizes.html")
@vcv.route('/logout')
def logout():
    a=open("current.txt",'w')
    a.seek(0)
    a.truncate()
    a.close()
    return render_template("logout.html")
@vcv.route('/select')
def select():
    return render_template("select.html")
@vcv.route('/select1')
def select1():
    return render_template("select2.html")
@vcv.route('/lib')
def lib():
    return render_template("lib.html")
@vcv.route('/cat')
def cat():
    return render_template("cat.html")

if __name__=="__main__":
    vcv.run(debug=True)
