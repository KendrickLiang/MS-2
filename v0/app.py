from flask import Flask, render_template, request, session, url_for, redirect, flash
import os
import db

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
	"viewPage": "viewPage.html"
}

def shortenArticleBody (numWords, body):
	count = 0
	newBody = ""
	bodyList = body.split()
	while (count < numWords):
		newBody += bodyList[count] + " "
		count+=1
	return newBody + "..."

#feed/login
@app.route("/", methods = ["POST", "GET"])
def input_field_page():
	if "username" in session:
		articles = db.getRandomEntries(db.getMyId(session["username"]))
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
			articleBodyShortened.append(shortenArticleBody(10, body))
		return render_template(fileNames["feed"], keys = articleKeys, titles = articleTitles, bodies = articleBodyShortened, username = session["username"]) #Still missing arguments that will be going in
	return render_template(fileNames["login"])

@app.route("/createaccount", methods=["POST"])
def create_account ():
	if (request.form['password'] == request.form['passwordConfirmation']):
		if not(db.checkUserInDatabase(request.form['username'])):
			flash("Username already taken")
			return redirect(url_for("sign_up_page"))
		else:
			flash("Account created successfully")
			db.addUserToDatabase(request.form['username'], request.form['password'])
			session['username']=request.form['username']
			return redirect(url_for("input_field_page"))
	else:
		flash("Password do not match")
		return redirect(url_for("sign_up_page"))


# def getRandomEntries ():
#     return {
#         	"1" : {"Awesome Post1" : "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi convallis ante sed lectus ultrices, eget accumsan augue consectetur. Nullam non urna et eros viverra aliquam vitae eu dui. Nulla a mauris fringilla, placerat orci vel, convallis nisi. Mauris dapibus euismod tempus. Etiam blandit nunc mi, quis tristique dui dapibus accumsan. Maecenas non hendrerit magna. Etiam at faucibus ante. Maecenas a volutpat dolor. In tristique libero id sagittis cursus. Mauris non viverra mi, in placerat purus."},
# 		"2" : {"Awesome Post2" : "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi convallis ante sed lectus ultrices, eget accumsan augue consectetur. Nullam non urna et eros viverra aliquam vitae eu dui. Nulla a mauris fringilla, placerat orci vel, convallis nisi. Mauris dapibus euismod tempus. Etiam blandit nunc mi, quis tristique dui dapibus accumsan. Maecenas non hendrerit magna. Etiam at faucibus ante. Maecenas a volutpat dolor. In tristique libero id sagittis cursus. Mauris non viverra mi, in placerat purus."},
# 		"3" : {"Awesome Post3" : "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi convallis ante sed lectus ultrices, eget accumsan augue consectetur. Nullam non urna et eros viverra aliquam vitae eu dui. Nulla a mauris fringilla, placerat orci vel, convallis nisi. Mauris dapibus euismod tempus. Etiam blandit nunc mi, quis tristique dui dapibus accumsan. Maecenas non hendrerit magna. Etiam at faucibus ante. Maecenas a volutpat dolor. In tristique libero id sagittis cursus. Mauris non viverra mi, in placerat purus."}
#         }

def getEntryByID(id):
	if (id == "1"):
		return {"Awesome Post1" : "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi convallis ante sed lectus ultrices, eget accumsan augue consectetur. Nullam non urna et eros viverra aliquam vitae eu dui. Nulla a mauris fringilla, placerat orci vel, convallis nisi. Mauris dapibus euismod tempus. Etiam blandit nunc mi, quis tristique dui dapibus accumsan. Maecenas non hendrerit magna. Etiam at faucibus ante. Maecenas a volutpat dolor. In tristique libero id sagittis cursus. Mauris non viverra mi, in placerat purus."}
	if (id == "2"):
		return {"Awesome Post2" : "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi convallis ante sed lectus ultrices, eget accumsan augue consectetur. Nullam non urna et eros viverra aliquam vitae eu dui. Nulla a mauris fringilla, placerat orci vel, convallis nisi. Mauris dapibus euismod tempus. Etiam blandit nunc mi, quis tristique dui dapibus accumsan. Maecenas non hendrerit magna. Etiam at faucibus ante. Maecenas a volutpat dolor. In tristique libero id sagittis cursus. Mauris non viverra mi, in placerat purus."}
	else:
		return {"Awesome Post3" : "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi convallis ante sed lectus ultrices, eget accumsan augue consectetur. Nullam non urna et eros viverra aliquam vitae eu dui. Nulla a mauris fringilla, placerat orci vel, convallis nisi. Mauris dapibus euismod tempus. Etiam blandit nunc mi, quis tristique dui dapibus accumsan. Maecenas non hendrerit magna. Etiam at faucibus ante. Maecenas a volutpat dolor. In tristique libero id sagittis cursus. Mauris non viverra mi, in placerat purus."}

@app.route("/login", methods = ["POST", "GET"])
def redirect_login ():
	return redirect(url_for("input_field_page"))

@app.route("/signup", methods = ["POST", "GET"])
def sign_up_page ():
	if "username" in session:
		return render_template(fileNames["feed"], articles = db.getRandomEntries(db.getMyId(session["username"])))
	return render_template(fileNames["signUp"])

#def addUserToDatabase (username, password):
    #print("Doing sutff")
	# Code by database role

@app.route("/auth", methods = ["POST"])
def auth_page():
	if db.login(request.form['username'], request.form['password']):
		session["username"] = request.form["username"]
	else:
		flash("Invalid Login Credentials.")
	return redirect(url_for("input_field_page"))


def getBlog (query):
	return {
		1: {query + '1': "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi convallis ante sed lectus ultrices, eget accumsan augue consectetur. Nullam non urna et eros viverra aliquam vitae eu dui. Nulla a mauris fringilla, placerat orci vel, convallis nisi. Mauris dapibus euismod tempus. Etiam blandit nunc mi, quis tristique dui dapibus accumsan. Maecenas non hendrerit magna. Etiam at faucibus ante. Maecenas a volutpat dolor. In tristique libero id sagittis cursus. Mauris non viverra mi, in placerat purus."},
		2: {query + '2': "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi convallis ante sed lectus ultrices, eget accumsan augue consectetur. Nullam non urna et eros viverra aliquam vitae eu dui. Nulla a mauris fringilla, placerat orci vel, convallis nisi. Mauris dapibus euismod tempus. Etiam blandit nunc mi, quis tristique dui dapibus accumsan. Maecenas non hendrerit magna. Etiam at faucibus ante. Maecenas a volutpat dolor. In tristique libero id sagittis cursus. Mauris non viverra mi, in placerat purus."},
		3: {query + '3': "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi convallis ante sed lectus ultrices, eget accumsan augue consectetur. Nullam non urna et eros viverra aliquam vitae eu dui. Nulla a mauris fringilla, placerat orci vel, convallis nisi. Mauris dapibus euismod tempus. Etiam blandit nunc mi, quis tristique dui dapibus accumsan. Maecenas non hendrerit magna. Etiam at faucibus ante. Maecenas a volutpat dolor. In tristique libero id sagittis cursus. Mauris non viverra mi, in placerat purus."}
	}

@app.route("/search", methods = ["GET", "POST"])
def search_page():
	if "username" not in session:
		return render_template(fileNames["login"])
	if ("searchQuery" in request.args):
		articles = getBlog(request.args["searchQuery"])
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
			articleBodyShortened.append(shortenArticleBody(10, body))
		return render_template(fileNames["search"], keys = articleKeys, titles = articleTitles, bodies = articleBodyShortened, username = session["username"])
	# print (request.args["queryString"])
	return render_template(fileNames["search"], username = session["username"])

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

@app.route ("/viewPage", methods = ["GET", "POST"])
def view_page():
	if "username" in session:
		print(request.args)
		if "entryId" in request.args:
			entry = getEntryByID(request.args["entryId"])
			return render_template(fileNames["viewPage"], title = list(entry.keys())[0], body = list(entry.values())[0], username = session["username"])
		else:
			return redirect(url_for("input_field_page"))
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
	flash("Edit saved")
	saveEntry(request.form['entryId'], request.form['title'], request.form['body'])
	return redirect(url_for("edit_page"))

@app.route("/createNewBlog", methods = ["POST"])
def create_new_blog ():
	print("hello")
	if "username" in session:
		if (checkIfBlogNameInUse(request.form["blogName"])):
			print("hello2")
			flash("Blog name already in use")
			return redirect(url_for("new_blog_page"))
		else:
			print("hello3")
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
