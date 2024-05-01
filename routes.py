#routes.py

from flask import render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from app import app, mysql
import pandas as pd

@app.route('/')
def hello():
	return render_template("index.html")

@app.route('/student')
def student_login():
	return render_template('student.html')

@app.route('/teacher')
def teacher_login():
	return render_template('teacher.html')

@app.route('/officer')
def officer_login():
	return render_template('officer.html')

@app.route('/student_dashboard', methods=['GET', 'POST'])
def student_dashboard():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute(
	'SELECT * FROM Users WHERE Username = %s AND PasswordHash = %s AND Role_ID = %s', 
	(username, password, 1))

		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['id'] = account['User_ID']
			session['username'] = account['Username']
			return render_template('student_dashboard.html')
		else:
			return redirect(url_for('student_login'))

@app.route('/teacher_dashboard', methods=['GET', 'POST'])
def teacher_dashboard():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute(
	'SELECT * FROM Users WHERE Username = %s AND PasswordHash = %s AND Role_ID = %s', 
	(username, password, 2))

		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['id'] = account['User_ID']
			session['username'] = account['Username']
			return render_template('teacher_dashboard.html')
		else:
			return redirect(url_for('teacher_login'))
	
@app.route('/officer_dashboard', methods=['GET', 'POST'])
def officer_dashboard():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute(
	'SELECT * FROM Users WHERE Username = %s AND PasswordHash = %s AND Role_ID = %s', 
	(username, password, 3))

		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['id'] = account['User_ID']
			session['username'] = account['Username']
			return render_template('officer_dashboard.html')
		else:
			return redirect(url_for('officer_login'))

@app.route('/display')
def display():
	if 'loggedin' in session:
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM Students WHERE User_ID = % s',(session['id'], ))
		account = cursor.fetchone()
		return render_template("display.html",account=account)
	return redirect(url_for('hello'))

@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('username', None)
	return redirect(url_for('hello'))


@app.route("/update", methods=['GET', 'POST'])
def update():
	msg = ''
	if 'loggedin' in session:
		if request.method == 'POST' and 'password' in request.form and 'email' in request.form and 'sem' in request.form and 'CGPA' in request.form and 'phone' in request.form:
			password = request.form['password']
			email = request.form['email']
			sem = request.form['sem']
			CGPA = request.form['CGPA']
			phone = request.form['phone']
			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor2= mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
				msg = 'Invalid email address !'
			elif not re.match(r'[0-9]+', phone):
				msg = 'phone must contain numbers !'
			else:
				cursor.execute('UPDATE Students SET Email =% s,Current_Semester =% s, CGPA =% s, phone =% s WHERE User_ID =% s', (email, sem, 
				CGPA, phone,(session['id'],),))
				mysql.connection.commit()
				cursor2.execute('UPDATE Users SET PasswordHash =% s WHERE User_Id=%s',(password,(session['id'],),))
				mysql.connection.commit()
				msg = 'You have successfully updated !'
		elif request.method == 'POST':
			msg = 'Please fill out the form !'
		return render_template("update.html", msg=msg)
	return redirect(url_for('hello'))

@app.route('/jobs')
def jobs():
	if 'loggedin' in session:
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM jobs')
		JOBS = cursor.fetchall()
		return render_template("jobs.html",JOBS=JOBS)
	return redirect(url_for('hello'))

@app.route("/complete", methods=['GET', 'POST'])
def complete():
	msg=""
	if 'loggedin' in session:
			if request.method == 'POST' and 'USN' in request.form and 'email' in request.form and 'department' in request.form and 'sem' in request.form and 'year' in request.form and 'CGPA' in request.form and 'graduation' in request.form and 'phone' in request.form and 'tenth' in request.form and 'twelfth' in request.form and 'aadhar' in request.form and 'PAN' in request.form and 'Linkedin' in request.form:
				USN=request.form['USN']
				email = request.form['email']
				department=request.form['department']
				sem = request.form['sem']
				year = request.form['year']
				CGPA = request.form['CGPA']
				graduation = request.form['graduation']
				phone = request.form['phone']
				tenth = request.form['tenth']
				twelfth = request.form['twelfth']
				aadhar = request.form['aadhar']
				PAN = request.form['PAN']
				Linkedin = request.form['Linkedin']
				cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

				if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
					msg = 'Invalid email address !'
				elif not re.match(r'[0-9]+', phone):
					msg = 'phone must contain numbers !'
				else:
					cursor.execute('UPDATE Students SET Email =% s,Current_Semester =% s, USN=%s, CGPA =% s, phone =% s ,Department =% s,Current_Year =% s, Year_of_Graduation =% s, Tenth_Percentage =% s,Twelfth_Percentage =% s,Aadhar_No =% s, PAN_No =% s, LinkedIn_ID =% s WHERE User_ID =% s', (email, sem, USN, CGPA, phone,department,year,graduation,tenth,twelfth,aadhar,PAN,Linkedin,(session['id'])))	
					mysql.connection.commit()
					msg = 'You have successfully updated !'
			elif request.method == 'POST':
				msg = 'Please fill out the form !'
			return render_template("complete_profile.html", msg=msg)
	return redirect(url_for('hello'))
@app.route('/apply')
def apply():
	if 'loggedin' in session:
		job_id = request.args.get('job_id')
		user_id=session['id']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('INSERT INTO applications (Job_ID,Student_ID) VALUES (%s,%s)',(job_id,user_id))
		mysql.connection.commit()
		return redirect(url_for('myapplications'))
	return redirect(url_for('hello'))

@app.route('/myapplications')
def myapplications():
	if 'loggedin' in session:
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM applications WHERE Student_ID = % s',(session['id'], ))
		apps= cursor.fetchall()
		return render_template("applications.html",apps=apps)
	return redirect(url_for('hello'))

@app.route('/studentslist')
def studentslist():
	if 'loggedin' in session:
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM Students')
		slist = cursor.fetchall()
		return render_template("s_list.html",slist=slist)
	return redirect(url_for('hello'))

@app.route('/allapplications')
def allapplications():
	if 'loggedin' in session:
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM applications')
		apps= cursor.fetchall()
		return render_template("all_applications.html",apps=apps)
	return redirect(url_for('hello'))

@app.route('/call_for_interview', methods=['GET', 'POST'])
def call_for_interview():
	if 'loggedin' in session:
		id = request.args.get('app_id')
		if request.method == 'POST' and 'date' in request.form and 'mode' in request.form:
			date=request.form['date']
			mode= request.form['mode']
			application_id = request.form['application_id']
			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute('INSERT INTO Interviews(Application_ID,Interview_Date,Interview_Type) VALUES (%s,%s,%s)',(application_id,date,mode))
			mysql.connection.commit()
			return render_template('officer_dashboard.html')
		return render_template("call_for_interview.html",id=id)
	
@app.route('/interviews')
def interviews():
	if 'loggedin' in session:
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM Interviews')
		interviews = cursor.fetchall()
		return render_template("interviews.html",interviews=interviews)
	return redirect(url_for('hello'))

@app.route('/officer_jobs')
def officer_jobs():
	if 'loggedin' in session:
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM jobs')
		JOBS = cursor.fetchall()
		return render_template("officer_jobs.html",JOBS=JOBS)
	return redirect(url_for('hello'))

@app.route('/all_companies')
def all_companies():
	if 'loggedin' in session:
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM companies')
		companies = cursor.fetchall()
		return render_template("companies.html",companies=companies)
	return redirect(url_for('hello'))

@app.route('/addjob', methods=['GET', 'POST'])
def addjob():
	if 'loggedin' in session:
		if request.method == 'POST' and 'Company_ID' in request.form and 'Position' in request.form and 'Job_Description' in request.form and 'Requirements' in request.form and 'Salary' in request.form and 'date' in request.form:
			Company_ID=request.form['Company_ID']
			Position= request.form['Position']
			Job_Description= request.form['Job_Description']
			Requirements= request.form['Requirements']
			Salary= request.form['Salary']
			date= request.form['date']
			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute('INSERT INTO Jobs(Company_ID, Position, Job_Description, Requirements, Salary, Deadline) VALUES (%s,%s,%s,%s,%s,%s)',(Company_ID,Position,Job_Description,Requirements,Salary,date))
			mysql.connection.commit()
			return redirect(url_for('officer_jobs'))
		return render_template("addjob.html")
	
@app.route('/addcompany', methods=['GET', 'POST'])
def addcompany():
	if 'loggedin' in session:
		if request.method == 'POST' and 'Company_ID' in request.form and 'Company_Name' in request.form and 'Industry' in request.form and 'Location' in request.form and 'Contact_Email' in request.form and 'Contact_Phone' in request.form and 'Website' in request.form:
			Company_ID=request.form['Company_ID']
			Company_Name= request.form['Company_Name']
			Industry= request.form['Industry']
			Location= request.form['Location']
			Contact_Email= request.form['Contact_Email']
			Contact_Phone= request.form['Contact_Phone']
			Website= request.form['Website']
			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute('INSERT INTO Companies(Company_ID, Company_Name, Industry, Location, Contact_Email, Contact_Phone, Website) VALUES (%s,%s,%s,%s,%s,%s,%s)',(Company_ID, Company_Name, Industry, Location, Contact_Email, Contact_Phone, Website))
			mysql.connection.commit()
			return redirect(url_for('all_companies'))
		return render_template("addcompany.html")

@app.route('/addstudent',methods=['GET', 'POST'])
def addstudent():
	if 'loggedin' in session:
		if request.method == 'POST' and 'User_id' in request.form and 'Username' in request.form and 'PasswordHash' in request.form:
			User_id=request.form['User_id']
			Username= request.form['Username']
			PasswordHash= request.form['PasswordHash']
			Role_ID=1
			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute('INSERT INTO Users(User_id,Username, PasswordHash, Role_ID) VALUES (%s,%s,%s,%s)',(User_id,Username, PasswordHash, Role_ID))
			mysql.connection.commit()
			return redirect(url_for('studentslist'))
		elif 'file' in request.files:
			file = request.files['file']
			print(file.filename)
			if file.filename != '':
				# Read the Excel file using pandas
				df = pd.read_excel(file)
				# Iterate through the rows and insert student records
				for index, row in df.iterrows():
					User_id = row['User_id']
					Username = row['Username']
					PasswordHash = row['PasswordHash']
					# print(f"User_id: {User_id}, Username: {Username}, PasswordHash: {PasswordHash}")

					Role_ID = 1								
					cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
					cursor.execute('INSERT INTO Users (User_id, Username, PasswordHash, Role_ID) VALUES (%s, %s, %s, %s)',
											(User_id, Username, PasswordHash, Role_ID))
					mysql.connection.commit()
			return redirect(url_for('studentslist'))
		return render_template("addstudent.html")
	
@app.route('/update_status',methods=['GET', 'POST'])
def update_status():
	if 'loggedin' in session:
		if request.method == 'POST' and 'status' in request.form and 'app_id' in request.form:
			app_id=request.form['app_id']
			status= request.form['status']
			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute('UPDATE interviews set Interview_Result=%s Where application_id=%s',(status,app_id))
			mysql.connection.commit()
			return redirect(url_for('interviews'))
		return render_template("officer_dashboard.html",id=id)