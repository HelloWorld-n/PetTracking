#!/usr/bin/python3
import cgitb, cgi
import CookieUtil
import pymysql
import Connect

owner = ""


form = cgi.FieldStorage(environ={'REQUEST_METHOD':'POST'})

print("content-type:text/html\n\n")
cgitb.enable()

print("""
<!DOCTYPE html>
<html lang="en">

<head>
	<meta charset="UTF-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<link rel="stylesheet" href="css/main.css">
	<title>Hello, world!</title>
	<script src="js/CookieUtil.js"></script>
	<script>
		let data = CookieUtil.getCookie()
	</script>
</head>

<body>
	<h1><a href="index.py">Main</a> / Modify Accounts</h1>
""")
if True:

	db = Connect.connectSql()
	try: 
		
		cursor = db.cursor()
		cursor.execute("USE db;")
		cursor.execute(
			(
				"SELECT * FROM owner"
			)
		)
		ownerUsername = cursor.fetchall()[0]["username"]
		cursor.execute(
			"SELECT * FROM users WHERE username = %s",
			[ownerUsername]
		)
		ownerPassword = cursor.fetchall()[0]["password"]
		if "submit" in form.keys() and form["username"].value == ownerUsername and form["password"].value == ownerPassword:
			if form["submit"].value in ["grantAdmin", "revokeAdmin"]:
				cursor.execute(
					(
						"UPDATE users SET "
							"isAdmin = %s "
						"WHERE username = %s "
					),
					[
						True if form["submit"].value == "grantAdmin" else False,
						form["accountUsername"].value,
					]
				)
				print("<h1 class=\"success\">Change succesfull.</h1>")
			else:
				print("<h1 class=\"failure\">Unknown command!</h1>")
		

		
		db.commit()
		db.close()
	except Exception as exception:
		print(exception)
		db.rollback()
		db.close()


	data = []
	db = Connect.connectSql()
	try: 
		cursor = db.cursor()
		cursor.execute("USE db;")
		cursor.execute(
			(
				"SELECT username, isAdmin FROM users"
			)
		)
		data = cursor.fetchall()
		db.rollback()
		db.close()
	except Exception:
		db.rollback()
		db.close()
	count = 0
	for info in data:
		count += 1
		print("""
			<form id="alter""" + str(count) + """" method="post" action="modifyAccounts.py">
				<input hidden id="username" name="username">
				<input hidden id="password" name="password">
				<input hidden id="accountUsername" name="accountUsername" value=""" + info["username"] + """>
				<div>""" + info["username"] + """</div>
				<script> 

					data = CookieUtil.getCookie()
					if(data["username"]){
						document.querySelectorAll("form#alter""" + str(count) + """ #username")[0].value = data["username"]
						document.querySelectorAll("form#alter""" + str(count) + """ #password")[0].value = data["password"]
					}
				</script>
				""" + ( 
					"""
						<div>
							<button type="submit" name="submit" value="grantAdmin" class="link-button">
								Grant admin privilegies!
							</button>
						</div>
					""" if info["isAdmin"] == 0 else """
						<div>
							<button type="submit" name="submit" value="revokeAdmin" class="link-button">
								Revoke admin privilegies!
							</button>
						</div>
					""" ) + 
				"""
			</form>
			<br/>
		""")
print("""
</body>
</html>
""")
