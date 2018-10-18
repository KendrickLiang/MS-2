from flask import Flask, render_template, request, session, url_for, redirect, flash
import os

app = Flask(__name__)
app.secret_key = os.urandom(32)

fileNames = {
	"search": "search.html",
	"edit": "edit.html",
	"login": "login.html",
	"feed": "feed.html"
}

@app.route("/", methods = ["POST", "GET"])
def input_field_page():
	if "username" in session:
		return render_template(fileNames["feed"]) #Still missing arguments that will be going in
	return render_template(fileNames["login"])

def checkUserInDatabase (username, password):
	# Code by database role

def addUserToDatabase (username, password):
	# Code by database role

@app.route("/auth", methods = ["POST"])
def auth_page():
	if checkUserInDatabase(request.form['username'], request.form['password']):
		session["username"] = request.form["username"]
	else:
		flash("Invalid Login Credentials.")
	return redirect(url_for("input_field_page"))

@app.route("/logout")
def logout():
	session.pop("username")
	flash("Logged out successfully")
	return redirect(url_for(fileNames["login"]))

if __name__ == "__main__":
	app.debug = True
	app.run()