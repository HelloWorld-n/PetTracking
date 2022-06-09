#!/usr/bin/python3
import HtmlTableUtil
import ListUtil
import pymysql
import cgitb, cgi
import Connect

global formCounter
formCounter = 0
print("content-type:text/html\n\n")
cgitb.enable()

form = cgi.FieldStorage(environ={'REQUEST_METHOD':'POST'})
def ticketInfo(ticket):
	global formCounter
	formCounter += 1
	if ticket["hidden"]:
		return ""
	return  f"""
		<table class="tg">
			
	
			<tbody>
				<tr>
					<td class="tg-td0d id">{ticket["id"]}</td>
					<td class="tg-td0d names">{HtmlTableUtil.html_escape(ticket["name"])}'s pet {HtmlTableUtil.html_escape(ticket["petName"])}</td>
				</tr>
				<tr>
					<td class="tg-td0d petDescription" colspan="3">
						{HtmlTableUtil.html_escape(ticket["petDescription"])}
					</td>
				</tr><tr>
					<td class="tg-td0d times" colspan="3">
						{HtmlTableUtil.html_escape("Post time: " + ticket["whenSubmit"].isoformat())}
						{(
							"<br/>" + HtmlTableUtil.html_escape("Time for callback: " + ticket["timeForCallBack"].isoformat())
						) if "timeForCallBack" in ticket.keys() and ticket["timeForCallBack"] != None else (
							""
						)}
					</td>
				</tr>
				<tr>
					<td class="tg-td0d" colspan="2"></td>
					<td class="tg-td0d">
						<form id="alter{formCounter}" method="post" action="viewSingleMissing.py">
							<input hidden name="id" value={ticket["id"]} />
							<input hidden id="username" name="username">
							<input hidden id="password" name="password">
							<script> 
								data = CookieUtil.getCookie()
								if(data["username"]){{
									document.querySelectorAll("form#alter{formCounter} #username")[0].value = (
										data["username"]
									) 
									document.querySelectorAll("form#alter{formCounter} #password")[0].value = (
										data["password"]
									)
								}}
							</script>
							<button type="submit" name="submit" value="view" class="link-button">
								View!
							</button>
						</form>
					</td>
				</tr>
			</tbody>
		</table>

	"""

print("""
<!DOCTYPE html>
<html lang="en">

<head>
	<meta charset="UTF-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<link rel="stylesheet" href="css/main.css">
	<title>View Tickets!</title>
	<style type="text/css">
		td.id {
			width: 5rem;
		}
		td.subject{
			width: 55rem;
		}
		td.name {
			width: 20rem;
		}
		td.problemDescription {
			width: 80rem;
			height: 10rem;
		}

		.tg {
			border-collapse: collapse;
			border-spacing: 0;
		}

		.tg td {
			border-style: solid;
			border-width: 1px;
			overflow: hidden;
			padding: 10px 5px;
			word-break: normal;
		}

		.tg th {
			border-style: solid;
			border-width: 1px;
			font-weight: normal;
			overflow: hidden;
			padding: 10px 5px;
			word-break: normal;
		}

		.tg .tg-td0d {
			text-align: left;
			vertical-align: top
		}
		
	</style>
	<script src="js/CookieUtil.js"></script>
</head>



<body>
	<script>
		let data
	</script>
	
	<h1><a href="index.py">Main</a> / View Missing Pets</h1>
	<h4>Sort By</h4>
	<div>
		<form method="post" action="viewMissing.py">
			<input hidden name="id" value={form["id"].value}/>
			
			<div>
				Post time: 
				<input type="radio" id="sortBy_whenSubmit" name="sortBy_whenSubmit" value="NONE" checked><label>NONE</label>
				<input type="radio" id="sortBy_whenSubmit" name="sortBy_whenSubmit" value="ASC"><label>ASC</label>
				<input type="radio" id="sortBy_whenSubmit" name="sortBy_whenSubmit" value="DESC"><label>DESC</label>
			</div><div>
				Preferered time for callback:
				<input type="radio" id="sortBy_timeForCallback" name="sortBy_timeForCallback" value="NONE" checked><label>NONE</label>
				<input type="radio" id="sortBy_timeForCallback" name="sortBy_timeForCallback" value="ASC"><label>ASC</label>
				<input type="radio" id="sortBy_timeForCallback" name="sortBy_timeForCallback" value="DESC"><label>DESC</label>
			</div>
		
			<input type="submit" name="sortBy">
			
		</form>
	</div>
""")
if True:
		db = Connect.connectSql()
		try:
			cursor = db.cursor()
			cursor.execute("USE db;")
			

			query = "SELECT * FROM missingPets WHERE hidden=False "
			if "sortBy" in form.keys():
				sortables = [
					"whenSubmit",
					"timeForCallback",
				]
				sorts = [form["sortBy_" + item] for item in sortables]
				sortValues = [item.value for item in sorts]
				if ListUtil.overlap(["ASC", "DESC"], sortValues):
					
					query += "ORDER BY "
					for item in sortables:
						query += (
							item + " " + 
							form["sortBy_"+item].value + ", "
						) if form["sortBy_"+item].value != "NONE" else (
							""
						)
					query = query[:-2]
			cursor.execute(query)
			for item in cursor.fetchall():
				print(ticketInfo(item) + "<br/>")

			db.commit()
		except Exception as exception:
			db.rollback()
			print(exception)
		db.close()


print("""
</body>


</html>
""")
