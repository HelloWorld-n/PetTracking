#!/usr/bin/python3
import pymysql
import cgitb, cgi
import Connect

print("content-type:text/html\n\n")
cgitb.enable()

form = cgi.FieldStorage(environ={'REQUEST_METHOD':'POST'})


print("""
<!DOCTYPE html>
<html lang="en">

<head>
	<meta charset="UTF-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<link rel="stylesheet" href="css/main.css">
	<title>Log in.</title>
	
</head>
<body>
	<h1><a href="index.py">Main</a> / Create account</h1>
""")
db = Connect.connectSql()
try:
	accountCreated = False
	problem = False
	cursor = db.cursor()
			
	cursor.execute("USE db;")
	
	if "create" in form.keys():
		cursor.execute("USE db;")

		cursor.execute("SELECT * FROM users WHERE username = %s", [form["username"].value])
		if len(cursor.fetchall()) > 0:
			print("<h1 class=\"failure\">There is already user with that username.</h1>")
			problem = True
		

		if form["password"].value != form["passwordSame"].value:
			print("<h1 class=\"failure\">Passwords are not same. </h1>")
			problem = True
		
		cursor.execute("SELECT * FROM users")
		data = cursor.fetchall()
		
		if not problem:
			cursor.execute(
				"""
					INSERT INTO users(username, password, isAdmin) VALUES (%s, %s, %s)
				""", 
				[
					form["username"].value,
					form["password"].value,
					len(data) < 1
				]
			)

		for testElement in [form["username"].value, form["password"].value]:
			if problem:
				break
			for char in testElement:
				if char in "<>&\\":
					print("<h1 class=\"failure\">Something contains weird characters.</h1>")
					print("<h1 class=\"failure\">Allowed: letters, digits, spaces, zal.</h1>")
					problem = True
					break

		if len(data) < 1:
			cursor.execute(
				"""
					INSERT INTO owner(username) VALUES (%s)
				""",
				[form["username"].value]
			)
				
		accountCreated = True

	if accountCreated and not problem:
		print("""
			<h1 class="success">Success.</h1>
			<a href="logIn.py">Log in.</h1>
		""")
		db.commit()
	else:
		print("""
			<form action="./createAccount.py" method="POST">
				<table><tbody>
				<tr>
					<td>Enter username: </td>
					<td><input name="username" type="text"></td>
				</tr><tr>
					<td>Enter password for altering access: </td>
					<td><input name="password" type="password"></td>
				</tr><tr>
					<td>Type same password as above: </td>
					<td><input name="passwordSame" type="password"></td>
				</tr><tr>
					<td></td><td><input name="create" type="submit"></td>
				</tr>
				</tbody></table>
			</form>
		""")

		db.rollback()
except Exception as exception:
	print("<h1 class=\"failure\">Problem.</h1>")
	print(exception)
	db.rollback()
db.close()

print("""
</body>
</html>
""")
