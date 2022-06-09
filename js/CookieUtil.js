class CookieUtil {

	static getCookie() {
		var output = {};
		document.cookie.split(/\s*;\s*/).forEach(function (pair) {
			pair = pair.split(/\s*=\s*/);
			output[pair[0].split(": ")[1]] = pair.splice(1).join('=')
		})
		return output

	}

	static clearCookie() {
		document.cookie.split(";").forEach(function (c) {
			document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/")
		})
	}

	static parseCookieText(text) {
		return text.replaceAll("\\q", "\"").replaceAll("\\s", ";").replaceAll("\\\\", "\\")
	}
}
