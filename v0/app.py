from flask import Flask, render_template, request, session, url_for, redirect, flash
import os

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
	"newEntry": "newentry.html"
}


@app.route("/", methods = ["POST", "GET"])
def input_field_page():
	if "username" in session:
		return render_template(fileNames["feed"], articles = getRandomBlogs(), username = session["username"]) #Still missing arguments that will be going in
	return render_template(fileNames["login"])

@app.route("/createaccount", methods=["POST"])
def create_account ():
	if (request.form['password'] == request.form['passwordConfirmation']):
		if (check_username_in_db(request.form['username'])):
			flash("Username already taken")
			return redirect(url_for("sign_up_page"))
		else:
			flash("Account created successfully")
			save_user_signup(request.form['username'], request.form['password'])
			return redirect(url_for("input_field_page"))
	else:
		flash("Password do not match")
		return redirect(url_for("sign_up_page"))

def check_username_in_db (username):
	return username == "test"

def save_user_signup (username, password):
	print("Saving " + username + " with password " + password)
# change to loginDatabase
def checkUserInDatabase (username, password):
    return True
	# Code by database role

def getRandomBlogs ():
    return {
        "Cool Title": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi convallis ante sed lectus ultrices, eget accumsan augue consectetur. Nullam non urna et eros viverra aliquam vitae eu dui. Nulla a mauris fringilla, placerat orci vel, convallis nisi. Mauris dapibus euismod tempus. Etiam blandit nunc mi, quis tristique dui dapibus accumsan. Maecenas non hendrerit magna. Etiam at faucibus ante. Maecenas a volutpat dolor. In tristique libero id sagittis cursus. Mauris non viverra mi, in placerat purus.",
        "Cool Title 2": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi convallis ante sed lectus ultrices, eget accumsan augue consectetur. Nullam non urna et eros viverra aliquam vitae eu dui. Nulla a mauris fringilla, placerat orci vel, convallis nisi. Mauris dapibus euismod tempus. Etiam blandit nunc mi, quis tristique dui dapibus accumsan. Maecenas non hendrerit magna. Etiam at faucibus ante. Maecenas a volutpat dolor. In tristique libero id sagittis cursus. Mauris non viverra mi, in placerat purus.",
        "Cool Title 3": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi convallis ante sed lectus ultrices, eget accumsan augue consectetur. Nullam non urna et eros viverra aliquam vitae eu dui. Nulla a mauris fringilla, placerat orci vel, convallis nisi. Mauris dapibus euismod tempus. Etiam blandit nunc mi, quis tristique dui dapibus accumsan. Maecenas non hendrerit magna. Etiam at faucibus ante. Maecenas a volutpat dolor. In tristique libero id sagittis cursus. Mauris non viverra mi, in placerat purus.",
        "Cool Title 4": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi convallis ante sed lectus ultrices, eget accumsan augue consectetur. Nullam non urna et eros viverra aliquam vitae eu dui. Nulla a mauris fringilla, placerat orci vel, convallis nisi. Mauris dapibus euismod tempus. Etiam blandit nunc mi, quis tristique dui dapibus accumsan. Maecenas non hendrerit magna. Etiam at faucibus ante. Maecenas a volutpat dolor. In tristique libero id sagittis cursus. Mauris non viverra mi, in placerat purus.",
        "Cool Title 5": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi convallis ante sed lectus ultrices, eget accumsan augue consectetur. Nullam non urna et eros viverra aliquam vitae eu dui. Nulla a mauris fringilla, placerat orci vel, convallis nisi. Mauris dapibus euismod tempus. Etiam blandit nunc mi, quis tristique dui dapibus accumsan. Maecenas non hendrerit magna. Etiam at faucibus ante. Maecenas a volutpat dolor. In tristique libero id sagittis cursus. Mauris non viverra mi, in placerat purus."
        }

@app.route("/login", methods = ["POST", "GET"])
def redirect_login ():
	return redirect(url_for("input_field_page"))

@app.route("/signup", methods = ["POST", "GET"])
def sign_up_page ():
	if "username" in session:
		return render_template(fileNames["feed"], articles = getRandomBlogs())
	return render_template(fileNames["signUp"])

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


def getBlog (query):
	return {
		query + '1': "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi convallis ante sed lectus ultrices, eget accumsan augue consectetur. Nullam non urna et eros viverra aliquam vitae eu dui. Nulla a mauris fringilla, placerat orci vel, convallis nisi. Mauris dapibus euismod tempus. Etiam blandit nunc mi, quis tristique dui dapibus accumsan. Maecenas non hendrerit magna. Etiam at faucibus ante. Maecenas a volutpat dolor. In tristique libero id sagittis cursus. Mauris non viverra mi, in placerat purus.",
		query + '2': "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi convallis ante sed lectus ultrices, eget accumsan augue consectetur. Nullam non urna et eros viverra aliquam vitae eu dui. Nulla a mauris fringilla, placerat orci vel, convallis nisi. Mauris dapibus euismod tempus. Etiam blandit nunc mi, quis tristique dui dapibus accumsan. Maecenas non hendrerit magna. Etiam at faucibus ante. Maecenas a volutpat dolor. In tristique libero id sagittis cursus. Mauris non viverra mi, in placerat purus.",
		query + '3': "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi convallis ante sed lectus ultrices, eget accumsan augue consectetur. Nullam non urna et eros viverra aliquam vitae eu dui. Nulla a mauris fringilla, placerat orci vel, convallis nisi. Mauris dapibus euismod tempus. Etiam blandit nunc mi, quis tristique dui dapibus accumsan. Maecenas non hendrerit magna. Etiam at faucibus ante. Maecenas a volutpat dolor. In tristique libero id sagittis cursus. Mauris non viverra mi, in placerat purus."
	}

@app.route("/search", methods = ["GET", "POST"])
def search_page():
	if ("searchQuery" in request.args):
		return render_template(fileNames["search"], articles = getBlog(request.args["searchQuery"]), username = session["username"])
	# print (request.args["queryString"])
	if "username" in session:
		return render_template(fileNames["search"], username = session["username"])
	return render_template(fileNames["login"])

def getMyEntries (userId):
	myEntry = {
		"123" : {"Why cats are cool" : "Cats are the coolest animal"},
		"235" : {"How to become rich" : "Buy money"},
		"344" : {"Grapes are nasty" : "Grapes taste horrible!"}
	}
	return myEntry

def getMyID (username):
	return 121

@app.route("/edit", methods = ["GET", "POST"])
def edit_page():
	if "username" in session:
		if ("entryId" in request.args):
			idEntryV = request.args["entryId"];
			titleV = list(getMyEntries(getMyID(session["username"]))[idEntryV].keys())[0]
			bodyV = getMyEntries(getMyID(session["username"]))[idEntryV][titleV]
			return render_template(fileNames["editPage"], idEntry = idEntryV, title = titleV, body = bodyV, username = session["username"])
		return render_template(fileNames["edit"], entries = getMyEntries(getMyID(session["username"])), username = session["username"])
	return render_template(fileNames["login"])

@app.route("/newblog", methods = ["GET", "POST"])
def new_blog_page ():
	if "username" in session:
		return render_template(fileNames["newBlog"], username = session["username"])
	return render_template(fileNames["login"])

def saveEntry(entryId, newTitle, newBody):
	print(entryId)
	print(newTitle)
	print(newBody)

@app.route("/save", methods = ["POST"])
def save_entry ():
	saveEntry(request.form['entryId'], request.form['title'], request.form['body'])
	return redirect(url_for("edit_page"), username = session["username"])

@app.route("/createNewBlog", methods = ["POST"])
def create_new_blog ():
	if "username" in session:
		if (checkIfBlogNameInUse(request.form["blogName"])):
			flash("Blog name already in use")
			return redirect(url_for("new_blog_page"), username = session["username"])
		else:
			flash("Blog created")
			createNewBlog(request.form["blogName"])
			return redirect(url_for("input_field_page"))
	return render_template(fileNames["login"]) 

def checkIfBlogNameInUse (name):
	return name == "test"

@app.route("/newentry", methods = ["GET", "POST"])
def new_entry_page ():
	if "username" in session:
		return render_template(fileNames["newEntry"], myBlogs = get_my_blog_titles(getMyID(session["username"])), username = session["username"])
	return render_template(fileNames["login"])

@app.route("/createNewEntry", methods=["POST"])
def create_new_post():
	if "username" in session:
		flash("Post Created")
		add_post(request.form["blogID"], request.form["entryTitle"], request.form["entryBody"])
		return redirect(url_for("input_field_page"))
	return render_template(fileNames["login"])

def add_post (blogId, newEntryTitle, newEntryBody):
	print("Creating new post in blog" + blogId + " with title " + newEntryTitle)


def get_my_blog_titles (username):
	return {
		"123" : "Cat Lovers",
		"235" : "Billionaire Boys",
		"344" : "Fruit Haters"
	}

def createNewBlog (name):
	print ("Creating new blog with name: " + name)

@app.route("/logout")
def logout():
	session.pop("username")
	return redirect(url_for("input_field_page"))

if __name__ == "__main__":
	app.debug = True
	app.run()
