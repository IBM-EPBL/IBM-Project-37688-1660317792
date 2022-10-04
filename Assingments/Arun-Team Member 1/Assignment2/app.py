
from flask import Flask, render_template, request, redirect,flash,url_for
import sqlite3 as sql

app = Flask(__name__)
app.secret_key = 'hdhrejrshrt'


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=='POST':
        eL=request.form['email']
        pW=request.form['password']
        con=sql.connect("database.db")
        con.row_factory=sql.Row
        cur=con.cursor()
        cur.execute("select * from registerDetails where email=? and password=?",(eL,pW))
        data=cur.fetchone()
        return redirect(url_for('index'))
        
    
    else:
        return render_template('login.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
            fn=request.form['firstname']
            ln=request.form['lastname']
            email=request.form['email']
            password=request.form['password']
            con=sql.connect("database.db")
            cur=con.cursor()
            cur.execute("INSERT INTO registerDetails (firstname,lastname,email,password) values(?,?,?,?)",(fn,ln,email,password))
            con.commit()
            return redirect(url_for('login'))
            con.close() 

    else:
        return render_template('register.html')
                          
