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
		return render_template(fileNames["feed"], articles = getRandomBlogs()) #Still missing arguments that will be going in
	return render_template(fileNames["login"])

def checkUserInDatabase (username, password):
    return True
	# Code by database role

def getRandomBlogs ():
    return {
        "Cool Title": "Awesome sause"
        }
#def addUserToDatabase (username, password):
    #print("Doing sutff")
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
    print("hello?")
    session.pop("username")
	#flash("Logged out successfully")
    return redirect(url_for("input_field_page"))

if __name__ == "__main__":
	app.debug = True
	app.run()
