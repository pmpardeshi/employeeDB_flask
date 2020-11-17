from flask import Flask, render_template, request, redirect, url_for, flash, abort, session, g
from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import time
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employee.db'
db = SQLAlchemy(app)

class Employee(db.Model):
    empId = db.Column(db.Integer, primary_key=True, nullable=False)
    empName = db.Column(db.String(20), nullable=False, default='N/A')
    empAddress = db.Column(db.String(100), nullable=False, default='N/A')
    empDOB = db.Column(db.String(10), nullable=False,default='N/A')
    empMobile = db.Column(db.Integer, nullable=False,default='N/A')

    def __repr__(self):
        return 'Employee ' + str(self.empId)

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
        new_record = Employee(empId=new_empId,empName=new_empName,empAddress=new_empAddress,empDOB=new_empDOB,empMobile=new_empMobile)
        db.session.add(new_record)
        db.session.commit()
        message = "Employee added successfully!"
        return render_template('add.html',message=message)
    return render_template('add.html')

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
