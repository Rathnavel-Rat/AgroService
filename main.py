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


@app.route('/')
def log():
    return render_template('login.html')
@app.route('/home')
def home():
    return render_template('home.html',msg=session['emailaddress'])
@app.route('/', methods=['GET', 'POST'])
def login():
        if 'loggedin' in session and session['loggedin']:
            return redirect(url_for('home'))
        msg = ''
        if request.method == 'POST':
            emailaddress = request.form['emailaddress']
            password = request.form['password']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM register WHERE emailaddress = % s AND password = % s',
                           (emailaddress, password))
            register = cursor.fetchone()

            if register:
                session['loggedin'] = True
                session['emailaddress'] = register["emailaddress"]
                return redirect(url_for('home'))
            else:
                msg = 'Incorrect emailaddress / password !'
                return render_template('login.html', msg=msg)

@app.route('/register', methods=['POST', 'GET'])
def register():
    if session["loggedin"]:
        return redirect(url_for('home'))
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
        else:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO register (name,emailaddress,phoneno,password) VALUES (%s,%s,%s,%s)",
                        (firstname, emailaddress, phoneno, password))
            mysql.connection.commit()
            cur.close()
            ms3 = 'You have successfully registered !'
            flash(ms3)
        return redirect(url_for('login'))
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg=msg)


@app.route('/admin/')
def adhome():
    return render_template('adminlog.html')


@app.route('/admin/', methods=['GET', 'POST'])
def adlogin():
        if 'loggedin' in session and session['loggedin']:
            return redirect(url_for('adminmain'))
        if request.method == 'POST':
            msg=''
            emailaddress = request.form['emailaddress']
            password = request.form['password']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM adregister WHERE emailaddress = % s AND password = % s',
                           (emailaddress, password))
            register = cursor.fetchone()

            if register:
                session['loggedin'] = True
                session['emailaddress'] = register["emailaddress"]
                return redirect(url_for('adminmain'))
            else:
                msg = 'Incorrect emailaddress / password !'
                return render_template('adminlog.html', msg=msg)
@app.route("/adminmain")
def adminmain():
    return render_template('main.html',msg=session['emailaddress'])

@app.route('/adminregister', methods=['POST', 'GET'])
def adregister():
    if 'loggedin' in session and session['loggedin']:
       return redirect(url_for('adminmain'))
    msg=''
    if request.method == 'POST' and 'password' in request.form and 'emailaddress' in request.form:
        firstname = request.form['firstname']
        emailaddress = request.form['emailaddress']
        phoneno = request.form['phoneno']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM adregister WHERE emailaddress = % s AND password = % s', (emailaddress, password))
        registers = cursor.fetchone()
        if registers:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', emailaddress):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', emailaddress):
            msg = 'Username must contain only characters and numbers !'
        else:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO adregister (name,emailaddress,phoneno,password) VALUES (%s,%s,%s,%s)",
                        (firstname, emailaddress, phoneno, password))
            mysql.connection.commit()
            cur.close()
            ms3 = 'You have successfully registered !'
            flash(ms3)
            return redirect('/admin/')
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('adminregister.html', msg=msg)



@app.route("/logout")
def logout():
    session['loggedin'] = False
    session['emailaddress'] = ""
    return redirect(url_for('login'))

@app.route("/adlogout")
def adlogout():
    session['loggedin'] = False
    session['emailaddress'] = ""
    return redirect(url_for('adlogin'))

@app.route("/aboutus")
def aboutus():
    return render_template('about.html',msg=session['emailaddress'])


@app.route("/galllery")
def gallery():
    return render_template('products.html',msg=session['emailaddress'])


@app.route("/contactus")
def contactus():
    return render_template('contact-us.html',msg=session['emailaddress'])


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp3', 'wav'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload/')
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
            ms='File successfully uploaded'
            flash((ms) + file.filename + ' to the database!')
            return render_template("upload1.html", msg=session['emailaddress'])
        else:
            ms = 'Invalid Uplaod only txt, pdf, png, jpg, jpeg, gif'
            flash(ms)
    return render_template("upload1.html",msg=session['emailaddress'])


@app.route("/Rent")
def Rent():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM product')
    products = cursor.fetchall()
    return render_template('Rent.html', product=products,msg=session['emailaddress'])


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
def orders():
    jsony = json.loads(request.data)
    data_ = json.dumps(jsony['order'])
    print(data_)
    total_ = jsony['total']

    cur = mysql.connection.cursor()
    mail = session['emailaddress']
    cur.execute("INSERT INTO orderdet (emailaddress,data,total) VALUES (%s,%s,%s)", (mail, data_, str(total_)))
    mysql.connection.commit()
    cur.close()
    return render_template('Rent.html')

@app.route("/placedorders",)
def placedorders():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM orderdet WHERE emailaddress=%s',[session['emailaddress']])
    orders= cur.fetchall()
    cur.close()
    return render_template('placedorders.html', date=orders,msg=session['emailaddress'])
@app.route("/orderitems/<date>")
def orderitems(date):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM orderdet WHERE emailaddress=%s AND date=%s', ([session['emailaddress']],[date]))
    orders = cur.fetchone()
    ordereditem=json.dumps(json.loads(orders["data"]))

    cur.execute("select * from product ")
    product=cur.fetchall()
    cur.close()

    return  render_template('ordereditems.html',product=json.dumps(product),orders=orders,data=ordereditem,msg=session['emailaddress'])
if __name__ == '__main__':
    app.run(debug=True)
