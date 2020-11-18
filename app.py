from flask import Flask, render_template, request, redirect, flash, session
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'empdb'    #Statements for establishing connection to mysql database
mysql = MySQL(app)
app.secret_key='daffjsdfyi76487pa'  #Used for flashing messages

@app.route("/") #First route to be displayed when webapp is loaded
def hello():
    return redirect('/alldata')

@app.route("/add", methods=['GET','POST'])  #Add employee
def add():
    if request.method=='POST':
        new_empId = request.form['empid']
        new_empName = request.form['name']
        new_empAddress = request.form['address']
        new_empDOB = request.form['dob']
        new_empMobile = request.form['mobile']  #Store data from the form

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO employee(empid, empname, empaddress, empdob, empmobile) VALUES (%s, %s, %s, %s, %s)", (int(new_empId), new_empName, new_empAddress, new_empDOB, new_empMobile))
        mysql.connection.commit()
        cur.close()

        flash(f'{new_empName} added successfully!',category='success')
        return redirect('/alldata')
    return render_template('add.html')

@app.route("/redirectpage", methods=['GET', 'POST'])    #Search id for updation and deletion
def redirectpage():
    if request.method == 'POST':
        if request.form['sbutton'] == 'Update': #If update button is clicked
            queryid = request.form['queryid']
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM employee WHERE empid=%s", (int(queryid),))
            data = cur.fetchall()
            if(data):
                session['queryvar']=data[0][0]  #Stored the id of the record to be updated in session variable to be accessed from /update
                return render_template('update.html', value=data)
            else:
                flash('No record found with entered ID',category='danger')
        else:   #If delete button is clicked
            queryid = request.form['queryid']
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM employee WHERE empid=%s", (int(queryid),))
            data = cur.fetchall()
            
            if(data):
                session['queryvar'] = int(data[0][0])   #Stored the id of the record to be deleted in session variable to be accessed from /delete
                return render_template('delete.html', value=data)
            else:
                flash('No record found with entered ID',category='danger')
    return render_template('redirectpage.html')

@app.route("/delete", methods=['GET', 'POST'])  #Delete employee
def delete():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        delthis = session.get('queryvar')   #Access id from session
        cur.execute("DELETE FROM employee WHERE empid=%s", (delthis,))
        mysql.connection.commit()
        session.pop('queryval', None)   #Remove id from session
        flash(f'Deleted record with ID: {delthis}',category='danger')
        return redirect('/alldata')
    return render_template('delete.html')

@app.route("/update", methods=['GET', 'POST'])  #Update employee details
def update():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        updthis = session.get('queryvar')   #Access id from session
        newname= request.form['name']
        newaddress = request.form['address']
        newmobile = request.form['mobile']
        sql_update_query = "UPDATE employee SET empname=%s, empaddress=%s ,empmobile=%s WHERE empid=%s"
        input_data=(newname, newaddress, newmobile, updthis)
        cur.execute(sql_update_query, input_data)
        mysql.connection.commit()
        session.pop('queryval', None)   #Remove id from session
        flash(f'Updated record with ID: {updthis}',category='success')
        return redirect('/alldata')
    return render_template('update.html')

@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.method=='POST':
        cur=mysql.connection.cursor()

        if 'id' in request.form:
            idvar=int(request.form['id'])
            cur.execute("select * from employee where empid=%s",(idvar,))  #Search based on employee ID
            
        elif 'initials' in request.form:
            temp=request.form['initials']
            inivar=temp + "%"
            cur.execute("select * from employee where empname like %s",(inivar,))    #Search based on first letter of name
           
        elif 'age' in request.form:
            agevar=int(request.form['age'])
            cur.execute("select * from Employee where SUBSTRING(empdob,1,4) = YEAR(CURDATE())-%s",(agevar,))   #Search based on employee age
            
        
        Details=cur.fetchall()

        if Details:
            return render_template('detailsTable.html', Details=Details)
        else:
            flash(f'No record found of given data',category='danger')
    return render_template('search.html')



@app.route("/details/<int:id1>", methods=['GET', 'POST'])   #Display the record in detail for the clicked name
def details(id1):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM employee WHERE empid=%s", (int(id1),))
    data = cur.fetchall()
    print(data)
    session['queryvar']=data[0][0]
    return render_template('details.html', value=data)
      


@app.route("/alldata", methods=['GET', 'POST']) #Display all available records in the database
def alldata():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM employee")
    Details = cur.fetchall()
    return render_template('alldata.html', Details=Details)
        






