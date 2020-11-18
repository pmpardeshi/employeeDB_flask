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
        # message = "Employee added successfully!"
        flash('Employee added successfully!',category='success')
        return render_template('add.html')
    return render_template('add.html')

@app.route("/redirectpage", methods=['GET', 'POST'])
def redirectpage():
    if request.method == 'POST':
        if request.form['sbutton'] == 'Update':
            queryid = request.form['queryid']
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM employee WHERE empid=%s", (int(queryid),))
            data = cur.fetchall()
            if(data):
                session['queryvar']=data[0][0]
                return render_template('update.html', value=data)
            else:
                flash('No record found with entered ID',category='danger')
        else:
            queryid = request.form['queryid']
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM employee WHERE empid=%s", (int(queryid),))
            data = cur.fetchall()
            
            if(data):
                session['queryvar'] = int(data[0][0])
                return render_template('delete.html', value=data)
            else:
                flash('No record found with entered ID',category='danger')
    return render_template('redirectpage.html')

@app.route("/delete", methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        delthis = session.get('queryvar')
        cur.execute("DELETE FROM employee WHERE empid=%s", (delthis,))
        mysql.connection.commit()
        session.pop('queryval', None)
        flash(f'Deleted record with ID: {delthis}',category='danger')
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
        sql_update_query = "UPDATE employee SET empname=%s, empaddress=%s ,empmobile=%s WHERE empid=%s"
        input_data=(newname, newaddress, newmobile, updthis)
        cur.execute(sql_update_query, input_data)
        mysql.connection.commit()
        session.pop('queryval', None)        
        flash(f'Updated record with ID: {updthis}',category='success')
        return render_template('add.html')
    return render_template('update.html')

@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.method=='POST':
        cur=mysql.connection.cursor()

        if 'id' in request.form:
            idvar=int(request.form['id'])
            cur.execute("select * from employee where empid=%s",(idvar,))  #query for emp_id
            Details=cur.fetchall()
            return render_template('detailsTable.html', Details=Details)
        elif 'initials' in request.form:
            temp=request.form['initials']
            inivar=temp + "%"
            cur.execute("select * from employee where empname like %s",(inivar,))    #query for first_letter
            Details = cur.fetchall()
            return render_template('detailsTable.html', Details=Details)
        elif 'age' in request.form:
            agevar=int(request.form['age'])
            cur.execute("select * from Employee where SUBSTRING(empdob,1,4) = YEAR(CURDATE())-%s",(agevar,))   #query for emp_age
            Details = cur.fetchall()
            return render_template('detailsTable.html', Details=Details)
        if not cur.fetchall():
            return render_template('search.html',message = 'Incorrect Employee details')
        # Details=((1 , 'aa'  ,'a' ,'2020-11-17','1'),(11,'pr','nsk','2012-12-12','8888'),(12,'kr','nsk','2010-12-12','8888'))
        # return render_template('detailsTable.html',Details=Details)
    return render_template('search.html')



@app.route("/details/<int:id1>", methods=['GET', 'POST'])
def details(id1):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM employee WHERE empid=%s", (int(id1),))
    data = cur.fetchall()
    print(data)
    session['queryvar']=data[0][0]
    return render_template('details.html', value=data)
      






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
