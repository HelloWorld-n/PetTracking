#!/usr/bin/python3
import pymysql
import cgitb, cgi
import Connect
import CookieUtil

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
	
	<h1><a href="index.py">Main</a> / Log in</h1>
""")
db = Connect.connectSql()
try:
	problem = False
	cursor = db.cursor()
			
	cursor.execute("USE db;")
	
	if "logIn" in form.keys():
		cursor.execute("USE db;")
		cursor.execute("SELECT * FROM users WHERE username = %s", [form["username"].value])
		data = cursor.fetchall()
		if len(data) < 1:
			print("<h1 class=\"failure\">There is no user with that username.</h1>")
			problem = True

		if form["password"].value != data[0]["password"]:
			print("<h1 class=\"failure\">Passwords are not same. </h1>")
			problem = True


	
	if not problem and "logIn" in form.keys():
		CookieUtil.setCookie({
			"username": form["username"].value,
			"password": form["password"].value,
		})
		print("""
			<h1 class="success">Logged in.</h1>
			<a href="index.py">Main page</h1>
		""")
		db.commit()
	else:
		print("""
			<form action="./logIn.py" method="POST">
				<table><tbody>
				<tr>
					<td>Enter username: </td>
					<td><input name="username" type="text"></td>
				</tr><tr>
					<td>Enter password: </td>
					<td><input name="password" type="password"></td>
				</tr><tr>
					<td></td><td><input name="logIn" type="submit"></td>
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
