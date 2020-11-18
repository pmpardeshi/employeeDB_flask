from flask import Flask, render_template, request, redirect, url_for, flash, abort, session, g
from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from datetime import datetime
import time
import random

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'empdb'
mysql = MySQL(app)
app.secret_key='daffjsdfyi76487pa'
# class Employee(db.Model):
#     empId = db.Column(db.Integer, primary_key=True, nullable=False)
#     empName = db.Column(db.String(20), nullable=False, default='N/A')
#     empAddress = db.Column(db.String(100), nullable=False, default='N/A')
#     empDOB = db.Column(db.String(10), nullable=False,default='N/A')
#     empMobile = db.Column(db.Integer, nullable=False,default='N/A')
#
#     def __repr__(self):
#         return 'Employee ' + str(self.empId)

"""  def __init__(self,empId,empName,empAddress,empDOB,empMobile):
        self.empId=empId
        self.empName=empName
        self.empAddress=empAddress
        self.empDOB=empDOB
        self.empMobile=empMobile 
"""

@app.route("/")
def hello():
    return redirect('/add')

@app.route("/add", methods=['GET','POST'])
def add():
    if request.method=='POST':
        new_empId = request.form['empid']
        new_empName = request.form['name']
        new_empAddress = request.form['address']
        new_empDOB = request.form['dob']
        new_empMobile = request.form['mobile']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO employee(empid, empname, empaddress, empdob, empmobile) VALUES (%s, %s, %s, %s, %s)", (int(new_empId), new_empName, new_empAddress, new_empDOB, new_empMobile))
        #new_record = Employee(empId=new_empId,empName=new_empName,empAddress=new_empAddress,empDOB=new_empDOB,empMobile=new_empMobile)
        mysql.connection.commit()
        cur.close()
        message = "Employee added successfully!"
        return render_template('add.html',message=message)
    return render_template('add.html')

@app.route("/redirectpage", methods=['GET', 'POST'])
def redirectpage():
    if request.method == 'POST':
        if request.form['sbutton'] == 'Update':
            queryid = request.form['queryid']
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM employee WHERE empid=%s", (int(queryid),))
            data = cur.fetchall()
            session['queryvar']=data[0][0]
            return render_template('update.html', value=data)
        else:
            queryid = request.form['queryid']
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM employee WHERE empid=%s", (int(queryid),))
            data = cur.fetchall()
            session['queryvar'] = int(data[0][0])
            if(data):
                return render_template('delete.html', value=data)
            else:
                flash('No record found with entered ID')
    return render_template('redirectpage.html')

@app.route("/delete", methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        delthis = session.get('queryvar')
        cur.execute("DELETE FROM employee WHERE empid=%s", (delthis,))
        mysql.connection.commit()
        session.pop('queryval', None)
        return render_template('add.html')
    return render_template('delete.html')

@app.route("/update", methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        updthis = session.get('queryvar')
        newname= request.form['name']
        newaddress = request.form['address']
        newmobile = request.form['mobile']
        sql_update_query = "UPDATE employee SET empname=%s empaddress=%s empmobile=%s WHERE empid=%s"
        input_data=(newname, newaddress, newmobile, updthis)
        cur.execute(sql_update_query, input_data)
        mysql.connection.commit()
        session.pop('queryval', None)
        return render_template('add.html')
    return render_template('update.html')

# @app.route('xyz', methods=['GET','POST'])
# def update():
#     if request.method=='POST':
#         search_id = request.form['empId']
#         r = Employee.query.filter(Employee.empId == search_id).first()
#         if not r:
#             return render_template('search_for_customer.html')
#         r.empName = request.form['newempName']
#         r.empAddress = request.form['newempAddress']
#         r.empDOB = request.form['newempDOB']
#         r.empMobile = request.form['newempMobile']
#         db.session.commit()
#         message = "Employee details updated successfully!"
#         return render_template('xyz',r=r,message=message)
#
# @app.route('xyz', methods=['GET','POST'])
# def delete():
#     if request.method=='POST':
#         search_id=request.form['empId']
#         result=Employee.query.filter(Employee.empId == search_id).first()
#         if not result:
#             return render_template('xyz')
#         db.session.delete(result)
#         db.session.commit()
#         return render_template('xyz', result=result)
#     return render_template('xyz')
