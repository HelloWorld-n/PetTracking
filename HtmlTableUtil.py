#!/bin/python3
def html_table(content, tableTags=""):
	result = f"<div type='{str(type(content))[8:-2]}'>"
	if type(content) in [list, set, tuple, dict]:
		result += f"<table {tableTags}><tbody>"
		if type(content) == dict:
			for key, value in content.items():
				result += \
					f"<tr><td class='key'>{html_table(key)}</td>"\
					f"<td class='value'>{html_table(value)}</td></tr>"
		else:
			for item in content:
				result += f"<tr><td class='item'>{html_table(item)}</td></tr>"
		result += "</table></tbody>"
	else:
		try:
			result += content.__html_table__()
		except AttributeError:
			result += html_escape(content.__str__())
	return result + "</div>"

def html_escape(text):
	return text.replace("&", "&amp").replace("<", "&lt").replace(">", "&gt;")

if __name__ == "__main__":
	class TestData:
		def __html_table__(self):
			return "Hehe"
	print(html_table(TestData()))
