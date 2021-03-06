# MS^2
# Matthew Ming, Sajed Nahian. Stefan Tan, Michelle Tang
# SoftDev1 pd6
# P #00: Da Art of Storytellin'

from flask import Flask, render_template, request, session, url_for, redirect, flash
import os
from db import *

app = Flask(__name__)
app.secret_key = os.urandom(32)

fileNames = {
	"search": "search.html",
	"edit": "edit.html",
	"login": "login.html",
	"feed": "feed.html",
	"editPage": "editPage.html",
	"signUp": "signup.html",
	"newBlog": "newblog.html",
	"newEntry": "newentry.html",
	"newEntryError": "newentryerror.html",
	"viewPage": "viewPage.html"
}
# Returns a shortened version of the blog description
def shortenArticleBody (numWords, body):
	return body

@app.route("/", methods = ["POST", "GET"])
#feed/login
# access feed of logged-in user
def input_field_page():
	if "username" in session:
		articles = getRandomEntries(getMyId(session["username"]))
		articleKeys = list(articles.keys())
		articleTitles = []
		articleBody = [];
		for key in articles:
			#print (key)
			for title in articles[key]:
				articleTitles.append(title)
				articleBody.append(articles[key][title])
		#print (articleTitles)
		articleBodyShortened = [];
		for body in articleBody:
			articleBodyShortened.append(shortenArticleBody(20, body))
		return render_template(fileNames["feed"], keys = articleKeys, titles = articleTitles, bodies = articleBodyShortened, username = session["username"]) #Still missing arguments that will be going in
	return render_template(fileNames["login"])

@app.route("/createaccount", methods=["POST"])
#sign up page where password must be correctly written twice and password and username are unique
# redirects to login if account is succesfully Created
# else redirects back to signup page for another attempt
def create_account ():
	if (request.form['password'] == request.form['passwordConfirmation']):
		if not(addUserToDatabase(request.form['username'], request.form['password'])):
			flash("Username already taken")
			return redirect(url_for("sign_up_page"))
		else:
			flash("Account created successfully")
			# session['username']=request.form['username']
			return redirect(url_for("input_field_page"))
	else:
		flash("Password do not match")
		return redirect(url_for("sign_up_page"))

@app.route("/login", methods = ["POST", "GET"])
#allows facilitation of state of user and location.
def redirect_login ():
	return redirect(url_for("input_field_page"))

@app.route("/signup", methods = ["POST", "GET"])
#Sends user to feed page if already signed in
#else sends them to sign up page
def sign_up_page ():
	if "username" in session:
		return render_template(fileNames["feed"], articles = getRandomEntries(getMyId(session["username"])))
	return render_template(fileNames["signUp"])

@app.route("/auth", methods = ["POST"])
#login page that sends user back to login if fail credential match
#else sends user to their feed page
def auth_page():
	if login(request.form['username'], request.form['password']):
		session["username"] = request.form["username"]
	else:
		flash("Invalid Login Credentials.")
	return redirect(url_for("input_field_page"))

@app.route("/search", methods = ["GET", "POST"])
# Loads search page of specified name if logged on
# else redirects to login page
def search_page():
	if "username" not in session:
		return render_template(fileNames["login"])
	if ("searchQuery" in request.args):
		articles = getBlogs2(getMyId(session["username"]), request.args["searchQuery"])
		articleKeys = list(articles.keys())
		articleTitles = []
		articleBody = [];
		print("YIKES: " + str(articles))
		for key in articles:
			#print (key)
			for title in articles[key]:
				articleTitles.append(title)
				articleBody.append(articles[key][title])
		#print (articleTitles)
		articleBodyShortened = [];
		for body in articleBody:
			articleBodyShortened.append(shortenArticleBody(10, body))
		return render_template(fileNames["search"], keys = articleKeys, titles = articleTitles, bodies = articleBodyShortened, username = session["username"])
	# print (request.args["queryString"])
	return render_template(fileNames["search"], username = session["username"])

@app.route("/edit", methods = ["GET", "POST"])
# Accesses current user's edit page and allows them to edit only their own entries
# otherwise redirects to login page
def edit_page():
	if "username" in session:
		print("&&&&&&&&&" + str(getMyUserEntries(getMyId(session["username"]))))
		if ("entryId" in request.args):
			print("^^^^^^^^^^^^^^" + str(returnEntry(int(request.args["entryId"]))))
			idEntryV = request.args["entryId"];
			entryT = list(returnEntry(int(request.args["entryId"])).keys())
			titleV = entryT[0]
			entryB = list(returnEntry(int(request.args["entryId"])).values())
			bodyV = entryB[0]
			return render_template(fileNames["editPage"], idEntry = idEntryV, title = titleV, body = bodyV, username = session["username"])
		return render_template(fileNames["edit"], entries = getMyUserEntries(getMyId(session["username"])), username = session["username"])
	return render_template(fileNames["login"])

@app.route ("/viewPage", methods = ["GET", "POST"])
# Allows user to view individual blogs by other users
def view_page():
	if "username" in session:
		print(request.args)
		if "entryId" in request.args:
			entry = returnEntry(int(request.args["entryId"]))
			return render_template(fileNames["viewPage"], title = list(entry.keys())[0], body = list(entry.values())[0], username = session["username"])
		else:
			return redirect(url_for("input_field_page"))
	return render_template(fileNames["login"])

@app.route("/newblog", methods = ["GET", "POST"])
# Creates new blog page if logged on
# else redirects to login page
def new_blog_page ():
	if "username" in session:
		return render_template(fileNames["newBlog"], username = session["username"])
	return render_template(fileNames["login"])

@app.route("/save", methods = ["POST"])
# Saves blog entry and redirects to edit page
def save_entry ():
	flash("Edit saved")
	updateEntry(int(request.form['entryId']), request.form['title'], request.form['body'])
	return redirect(url_for("edit_page"))

# Creates new blog if name is unique
@app.route("/createNewBlog", methods = ["POST"])
def create_new_blog ():
	print("hello")
	if "username" in session:
		if not (checkIfBlogNameInUse(request.form["blogName"])):
			print("hello2")
			flash("Blog name already in use")
			return redirect(url_for("new_blog_page"))
		else:
			print("----------------------" + str(getMyId(session["username"])))
			flash("Blog created")
			addBlogToDatabase(getMyId(session["username"]), request.form["blogName"])
			return redirect(url_for("input_field_page"))
	return render_template(fileNames["login"])


@app.route("/newentry", methods = ["GET", "POST"])
# Creates new blog entry if logged on
# else redirects to login page
def new_entry_page ():
	if "username" in session:
		dictBlogs = {}
		myblogs = get_my_blog_titles(getMyId(session["username"]))
		if (len(myblogs) == 0):
			return render_template(fileNames["newEntryError"], username = session["username"])
		for blogtitle in myblogs:
			dictBlogs[blogID(blogtitle)] = blogtitle
		print("*******************" + str(myblogs))
		return render_template(fileNames["newEntry"], myBlogs = dictBlogs, username = session["username"])
	return render_template(fileNames["login"])


@app.route("/createNewEntry", methods=["POST"])
# Creates new blog post if logged on
# else redirects to login page
def create_new_post():
	if "username" in session:
		flash("Post Created")
		addEntryToDatabase(getMyId(session["username"]), int(request.form["blogID"]), request.form["entryTitle"].strip(), request.form["entryBody"].strip())
		return redirect(url_for("input_field_page"))
	return render_template(fileNames["login"])

@app.route("/logout")
#Pops user's current session and logs them out
def logout():
	session.pop("username")
	return redirect(url_for("input_field_page"))

if __name__ == "__main__":
	app.debug = True
	app.run()
