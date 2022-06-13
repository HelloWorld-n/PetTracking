#!/usr/bin/python3
import cgitb, cgi
import HtmlTableUtil
import pymysql
import datetime
import Connect
import CookieUtil
import DatabaseUtil

print("content-type:text/html\n\n")
cgitb.enable(logdir="./.logs.txt")

form = cgi.FieldStorage(environ={'REQUEST_METHOD':'POST'})

isAdminAccount = False

print("""
<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="UTF-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<link rel="stylesheet" href="css/main.css">
		<style>
			table[main] {
				width: 90%;
			}

			textarea {
				width: 50rem;
				height: 10rem;
			}
		</style>
		<script src="js/CookieUtil.js"></script>
		<title>missingPetCreator</title>
	</head>

	<body>
		<h1><a href="index.py">Main</a> / <a href="viewMissing.py">View Missing Pets</a> / View Specific Pet</h1>
""")
if True:
			db = Connect.connectSql()
			try:
				cursor = db.cursor()
				cursor.execute("USE db;")
				
				try:
					cursor.execute(
						(
							"SELECT * FROM users WHERE ("
								"username = %s"
							") AND ("
								"password = %s"
							") AND ("
								"isAdmin = true"
							")"
						),
						[
							form["username"].value,
							form["password"].value,
						]
					)
					data = cursor.fetchall()
				except KeyError:
					data = []


				if form["submit"].value == "comment":
					if len(data) > 0:
						cursor.execute(
							"UPDATE missingPets "
							"SET comment=%s "
							"WHERE id=%s ",
							[	
								form["comment"].value, 
								int(form["id"].value.replace("/", "")),
							]
						)
						print("<h1 class=\"success\">Comment changed!</h1>")
					else:
						print("<h1 class=\"failure\">This account is not admin!</h1>")
				elif form["submit"].value == "updateLastSeen":
					if len(data) > 0:
						cursor.execute(
							"UPDATE missingPets "
							"SET "
							"	timeLastSeen=%s, "
							"	locationLastSeen=Point(%s, %s) "
							"WHERE id=%s ",
							[	
								form["timeLastSeen"].value, 
								round(float(form["locationLastSeen_posX"].value), 4),
								round(float(form["locationLastSeen_posY"].value), 4),
								int(form["id"].value.replace("/", ""))
							]
						)
						print("<h1 class=\"success\">Comment changed!</h1>")
					else:
						print("<h1 class=\"failure\">This account is not admin!</h1>")
				elif form["submit"].value in ["hide", "archive"]:
					if len(data) > 0:
						cursor.execute(
							"UPDATE missingPets "
							"SET hidden=True "
							"WHERE id=%s",
							[int(form["id"].value.replace("/", ""))]
						)
						print("<h1 class=\"success\">Comment archieved!</h1>")
					else:
						print("<h1 class=\"failure\">This account is not admin!</h1>")
				
				
				data = DatabaseUtil.cleanDatabaseTable(cursor, "missingPets", form["id"].value)
				
				for item in ["hidden"]:
					if item in data:
						data[item] = bool(data[item])

				for item in data:
					print(HtmlTableUtil.html_table(item, tableTags="main"))
				
				db.commit()
			except Exception as exception:
				db.rollback()
				print("<h1 class=\"failure\">There has been problem!</h1>")
				print(exception)
				db.close()

try: 
	db = Connect.connectSql()
	cursor = db.cursor()
	cursor.execute("USE db;")
	cursor.execute(
		("""
			SELECT timeLastSeen as `theTime`, st_x(locationLastSeen) as `posX`, st_y(locationLastSeen) as `posY`
			FROM missingPets WHERE id = %s
		"""),
		[
			form["id"].value
		]
	)
	data = cursor.fetchall()
	theTime = data[0]["theTime"]
	posX = data[0]["posX"]
	posY = data[0]["posY"]
	db.rollback()
	cursor.execute(
		(
			"SELECT * FROM users WHERE ("
				"username = %s"
			") AND ("
				"password = %s"
			") AND ("
				"isAdmin = true"
			")"
		),
		[
			CookieUtil.parseCookieText(form["username"].value),
			CookieUtil.parseCookieText(form["password"].value),
		]
	)
	db.rollback()
	db.close()
	dataAdmin = cursor.fetchall()
	if len(dataAdmin) > 0:
		isAdminAccount = True
		print(f"""
			<br>
			<form id="alter" method="post" action="viewSingleMissing.py">
				<input hidden name="id" value=\"{form["id"].value}\">
				<input hidden id="username" name="username">
				<input hidden id="password" name="password">
				<script> 

					let data = CookieUtil.getCookie()
					if(data["username"]){{
						document.querySelectorAll("form#alter #username")[0].value = CookieUtil.parseCookieText(data["username"])
						document.querySelectorAll("form#alter #password")[0].value = CookieUtil.parseCookieText(data["password"])
					}}
				</script>
				<div>
					<textarea name="comment"></textarea>
				</div>
				<div>
					Seen <input type="datetime-local" id="timeLastSeen" name="timeLastSeen" value=\"{
						(
							str(theTime)
						if theTime else
							str(datetime.datetime.now().isoformat()) 
						)
					}\"/>
					at (
						<input type="number" step="0.0001" id="locationLastSeen_posX" name="locationLastSeen_posX" value=\"{
							(
								str(round(posX, 4))
							if posX else 
								"None"
							)
					}\"/>, 
						<input type="number" step="0.0001" id="locationLastSeen_posY" name="locationLastSeen_posY" value=\"{
							(
								str(round(posY, 4))
							if posY else 
								"None" 
							)
					}\"/>
					)
				</div>
				<div>
					<button type="submit" name="submit" value="comment" class="link-button">
						Comment!
					</button>
					<button type="submit" name="submit" value="updateLastSeen" class="link-button">
						Update LastSeen Info
					</button>
					<button type="submit" name="submit" value="hide" class="link-button">
						Archive!
					</button>
				</div>
			</form>
		""")
	else:
		"""
			Account is not admin.
		"""
except KeyError:
	"""
		Account is not even account.
	"""

if not isAdminAccount:
	print("""
		<br><br>
		<div>Current account is not admin.</div>
		<div>To alter data: <a href="logIn.py" onclick="CookieUtil.clearCookie()">Log in as admin.</a></div>
	""")
print("""
	</body>

</html>
""")
