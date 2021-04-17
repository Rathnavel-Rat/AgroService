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


@app.route("/")
def home():
    return render_template("login.html")


 
if __name__ == '__main__':
    app.run(debug=True)