#!/usr/bin/python3
import cgitb, cgi
import HtmlTableUtil
import pymysql
import datetime
import Connect

print("content-type:text/html\n\n")
cgitb.enable(logdir="./.logs.txt")

form = cgi.FieldStorage(environ={'REQUEST_METHOD':'POST'})

__DEBUG = []

print("""
<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="UTF-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<link rel="stylesheet" href="css/main.css">
		<style>

		</style>
		<title>Report Missing Pet</title>
	</head>

	<body>
		<h1><a href="index.py">Main</a> / Report Missing Pet (Status report)</h1>
""")
if True:
			data = {}
			for key in form.keys():
				data[key] = form[key].value
			if "data" in __DEBUG:
				print(HtmlTableUtil.html_table(data))
			db = Connect.connectSql()
			try:
				cursor = db.cursor()
				cursor.execute("USE db;")
			
				data_keys = ""
				data_percentEses = ""
				data_values = []
				data
				for item in data:
					data_keys += f"{item}, "
					data_percentEses += "%s, "
					data_values += [data[item]]
				data_keys = data_keys + "whenSubmit"
				data_percentEses = data_percentEses + f"'{datetime.datetime.now().isoformat()}'"
				cursor.execute(
					f"INSERT INTO missingPets ({data_keys}) VALUES ({data_percentEses})",
					data_values
				)
					
				db.commit()
				print("<h1 class=\"success\">Success!</h1>")
			except Exception as exception:
				db.rollback()
				print("<h1 class=\"failure\">There has been problem!</h1>")
				print(exception)
			db.close()
			

print("""
	</body>

</html>
""")
