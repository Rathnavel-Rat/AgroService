from flask import Flask, render_template, request, Response, session, flash, redirect, url_for, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
from werkzeug.utils import secure_filename
from flask import jsonify
import re, os
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/upload/'
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "agro"
app.secret_key = 'the random string'
app.config['secret_key'] = "dhfebfhuiu34h3u7rh387fh8723h7hr83h27h8"

mysql = MySQL(app)


@app.route('/home')
@app.route('/')
def home():
    if "loggedin" not in session:
        return render_template('home.html')
    return render_template('login.html')


@app.route('/', methods=['GET', 'POST'])
def login():
    if session["loggedin"]:
        return render_template('home.html')
    msg = ''
    if request.method == 'POST':
        emailaddress = request.form['emailaddress']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM register WHERE emailaddress = % s AND password = % s', (emailaddress, password))
        register = cursor.fetchone()

        if register:
            session['loggedin'] = True
            session['emailaddress'] = register["emailaddress"]
            return render_template('home.html')
        else:
            msg = 'Incorrect emailaddress / password !'
            return render_template('login.html', msg=msg)


@app.route('/register', methods=['POST', 'GET'])
def register():
    if session["loggedin"]:
        return render_template('home.html')
    msg = ''
    if request.method == 'POST' and 'password' in request.form and 'emailaddress' in request.form:
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
        else:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO register (name,emailaddress,phoneno,password) VALUES (,%s,%s,%s,%s)",
                        (firstname, emailaddress, phoneno, password))
            mysql.connection.commit()
            cur.close()
            msg = 'You have successfully registered !'
            return render_template('login.html', msg=msg)
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg=msg)


@app.route("/logout")
def logout():
    session['loggedin'] = False
    session['emailaddress'] = ""
    return render_template('login.html')


@app.route("/aboutus")
def aboutus():
    return render_template('about.html')


@app.route("/galllery")
def gallery():
    return render_template('gallery.html')


@app.route("/contactus")
def contactus():
    return render_template('contact-us.html')


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp3', 'wav'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == "POST":
        msg = ''
        file = request.files["file"]
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
        if file and allowed_file(file.filename):
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO product (id,productname,cost,image) VALUES (%s,%s,%s,%s)",
                        (request.form["id"], request.form["productname"], request.form["cost"], file.filename))
            mysql.connection.commit()
            cur.close()
            flash('File successfully uploaded ' + file.filename + ' to the database!')
            return render_template("upload1.html", msg='successfully uploaded')
        else:
            flash('Invalid Uplaod only txt, pdf, png, jpg, jpeg, gif')
    return render_template("upload1.html")


@app.route("/Rent")
def Rent():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM product')
    products = cursor.fetchall()
    return render_template('Rent.html',product=products)


@app.route("/display/<filename>")
def display_image(filename):
    h = 'image/gallery/' + filename
    flash(h)
    return redirect(url_for('static', filename=h), code=304)

@app.route("/Rent_display/<filename>")
def Rent_Display(filename):
    h = 'image/upload/' + "tract1.png"
    flash(h)
    return redirect(url_for('static', filename=h), code=304)

@app.route('/order/', methods=['GET', 'POST'])
@app.route('/order', methods=['GET', 'POST'])
def order():
    jsony=json.loads(request.data)
    data=json.dumps(jsony['order'])
    total=jsony['total']
    return  render_template('Rent.html')

if __name__ == '__main__':
    app.run(debug=True)
