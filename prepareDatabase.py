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
""")
try:
	db = Connect.connectSql()
	cursor = db.cursor()
	cursor.execute("CREATE DATABASE IF NOT EXISTS db;")
	cursor.execute("USE db;")
	cursor.execute(
		"CREATE TABLE IF NOT EXISTS missingPets ("
			"id Int NOT NULL AUTO_INCREMENT,"
			"name VarChar(100) NOT NULL,"
			"phoneNumber VarChar(20),"
			"email VarChar(255) NOT NULL,"
			"petName VarChar(255) NOT NULL,"
			"petDescription Text(65536) NOT NULL,"
			"petMoreInfo Text(65536) NOT NULL,"
			"comment VarChar(4096) DEFAULT '',"
			"whenSubmit DateTime,"
			"timeLastSeen DateTime,"
			"locationLastSeen Point,"
			"hidden Boolean DEFAULT FALSE,"
			"PRIMARY KEY(id)"
		")"
	)


	cursor.execute(
		"CREATE TABLE IF NOT EXISTS users ("
			"username VarChar(255) NOT NULL,"
			"password VarChar(255) NOT NULL,"
			"isAdmin TinyInt(1) DEFAULT false,"
			"PRIMARY KEY(username)"
		")"
	)

	cursor.execute(
		"CREATE TABLE IF NOT EXISTS owner ("
			"username VarChar(255) NOT NULL,"
			"PRIMARY KEY(username)"
		")"
	)


	print("""
		<a href="index.py">Main</a>
		<a href="createAccount.py">Create account</a>
	""")

	db.commit()
except Exception as exception:
	print("<h1 class=\"failure\">Problem.</h1>")
	print(exception)

print("""
</body>
</html>
""")
