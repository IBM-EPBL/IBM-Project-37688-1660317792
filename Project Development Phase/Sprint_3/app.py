from flask import Flask,render_template,url_for,redirect,session,request
import ibm_db,re

app = Flask(__name__)
app.secret_key = "edfgdhsjkueme"

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/login, methods=['GET', 'POST']")
def login():
    if request.method == "POST":
        global message

        user = request.form
        print(user)
        email = user["email"]
        password = user["password"]

        print("Email - " + email + ", Password - " + password)

        sql = "SELECT * FROM users WHERE email = ? AND password = ?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, email)
        ibm_db.bind_param(stmt, 2, password)
        ibm_db.execute(stmt)

        account = ibm_db.fetch_assoc(stmt)
        print("Account - ")
        print(account)

        if account:
            session['loggedin'] = True
            session['id'] = account['EMAIL']
            user_email = account['EMAIL']
            session['email'] = account['EMAIL']
            session['name'] = account['NAME']

            return redirect(url_for('tracker'))

        else:
            message = "Incorrect Email or Password"
            return redirect(url_for('/signup'))

    return render_template('login.html')

@app.route("/signup, methods=['GET', 'POST']")
def signup():
    if request.method == "POST":
        global message

        user = request.form
        print(user)
        name = user["name"]
        email = user["email"]
        password = user["password"]

        sql = "SELECT * FROM USERS WHERE email = ?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, email)
        ibm_db.execute(stmt)

        account = ibm_db.fetch_assoc(stmt)
        print("Account - ", end="")
        print(account)

        if account:
            message = "Account already exists"
            return redirect(url_for('home', page="register"))
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            message = "Invalid email address"
            return redirect(url_for('home', page="register"))
        elif not re.match(r'[A-Za-z0-9]+', name):
            message = "Name must contain only characters and numbers"
            return redirect(url_for('home', page="register"))
        else:
            insert_sql = "INSERT INTO users VALUES (?, ?, ?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, name)
            ibm_db.bind_param(prep_stmt, 2, email)
            ibm_db.bind_param(prep_stmt, 3, password)
            ibm_db.execute(prep_stmt)

            session['loggedin'] = True
            session['id'] = email
            user_email = email
            session['email'] = email
            session['name'] = name

            message = ""

            return redirect(url_for('/dashboard'))
    return render_template('signup.html')

@app.route("/dashboard")
def signup():
    return render_template('dashboard.html')   

@app.route('/logout')
def logout():
    print("Logging Out")
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('email', None)
    session.pop('name', None)
    return redirect(url_for('/index'))    



