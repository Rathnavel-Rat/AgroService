from flask import Flask,render_template,request,Response,session,flash,redirect,url_for,flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
from flask import jsonify
import re,os
import json
app=Flask(__name__)
app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']=""
app.config['MYSQL_DB']="agro"
app.secret_key = 'the random string'
app.config['secret_key']="dhfebfhuiu34h3u7rh387fh8723h7hr83h27h8"


mysql=MySQL(app)


@app.route('/')
def home():
     return render_template('login.html') 

@app.route('/', methods =['GET', 'POST']) 
def login():
    msg = '' 
    print(request.method)
    if request.method == 'POST': 
        emailaddress = request.form['emailaddress'] 
        password = request.form['password'] 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('SELECT * FROM register WHERE emailaddress = % s AND password = % s', (emailaddress, password)) 
        register = cursor.fetchone()
        print(emailaddress)
        if register: 
            session['loggedin'] = True
            session['emailaddress'] = register["emailaddress"] 
            return render_template('home.html')
        else: 
            msg = 'Incorrect emailaddress / password !'
            return render_template('login.html',msg = msg)

@app.route('/index',methods = ['POST', 'GET'])
def index():
     
    return render_template('index.html',msg=session["emailaddress"])           

@app.route('/register',methods = ['POST', 'GET'])
def register():
    msg = ''
    print(request)
    if request.method == 'POST'and 'password' in request.form and 'emailaddress' in request.form:
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        emailaddress = request.form['emailaddress']
        phoneno = request.form['phoneno']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('SELECT * FROM register WHERE emailaddress = % s AND password = % s', (emailaddress, password)) 
        registers = cursor.fetchone()
        if registers:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', emailaddress):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', emailaddress):
            msg = 'Username must contain only characters and numbers !'
        elif not emailaddress or not password :
            msg = 'Please fill out the form !'
        else:
            cur=mysql.connection.cursor()
            cur.execute("INSERT INTO register (firstname,lastname,emailaddress,phoneno,password) VALUES (%s,%s,%s,%s,%s)",(firstname,lastname,emailaddress,phoneno,password))
            mysql.connection.commit()
            cur.close()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)


@app.route('/', methods =['GET', 'POST']) 
def login():
    msg = '' 
    if request.method == 'POST': 
        emailaddress = request.form['emailaddress'] 
        password = request.form['password'] 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('SELECT * FROM register WHERE emailaddress = % s AND password = % s', (emailaddress, password)) 
        register = cursor.fetchone()
         
        print(register)
        if register: 
            session['loggedin'] = True
            session['emailaddress'] = register["emailaddress"] 
            return render_template('home.html')
        else: 
            msg = 'Incorrect emailaddress / password !'
            return render_template('login.html',msg = msg)

@app.route('/register',methods = ['POST', 'GET'])
def register():
    msg = ''
    print(request)
    if request.method == 'POST'and 'password' in request.form and 'emailaddress' in request.form:
        firstname = request.form['name']
        emailaddress = request.form['emailaddress']
        phoneno = request.form['phoneno']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('SELECT * FROM register WHERE emailaddress = % s AND password = % s', (emailaddress, password)) 
        registers = cursor.fetchone()
        if registers:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', emailaddress):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', emailaddress):
            msg = 'Username must contain only characters and numbers !'
        elif not emailaddress or not password :
            msg = 'Please fill out the form !'
        else:
            cur=mysql.connection.cursor()
            cur.execute("INSERT INTO register (name,emailaddress,phoneno,password) VALUES (,%s,%s,%s,%s)",(firstname,emailaddress,phoneno,password))
            mysql.connection.commit()
            cur.close()
            msg = 'You have successfully registered !'
            return render_template('login.html',msg = msg)
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)



 
if __name__ == '__main__':
    app.run(debug=True)