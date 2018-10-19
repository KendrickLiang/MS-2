from flask import Flask, render_template, request, session, url_for, redirect, flash
import os

app = Flask(__name__)
app.secret_key = os.urandom(32)

fileNames = {
	"search": "search.html",
	"edit": "edit.html",
	"login": "login.html",
	"feed": "feed.html",
	"editPage": "editPage.html"
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
        "Cool Title": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi convallis ante sed lectus ultrices, eget accumsan augue consectetur. Nullam non urna et eros viverra aliquam vitae eu dui. Nulla a mauris fringilla, placerat orci vel, convallis nisi. Mauris dapibus euismod tempus. Etiam blandit nunc mi, quis tristique dui dapibus accumsan. Maecenas non hendrerit magna. Etiam at faucibus ante. Maecenas a volutpat dolor. In tristique libero id sagittis cursus. Mauris non viverra mi, in placerat purus.",
        "Cool Title 2": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi convallis ante sed lectus ultrices, eget accumsan augue consectetur. Nullam non urna et eros viverra aliquam vitae eu dui. Nulla a mauris fringilla, placerat orci vel, convallis nisi. Mauris dapibus euismod tempus. Etiam blandit nunc mi, quis tristique dui dapibus accumsan. Maecenas non hendrerit magna. Etiam at faucibus ante. Maecenas a volutpat dolor. In tristique libero id sagittis cursus. Mauris non viverra mi, in placerat purus.",
        "Cool Title 3": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi convallis ante sed lectus ultrices, eget accumsan augue consectetur. Nullam non urna et eros viverra aliquam vitae eu dui. Nulla a mauris fringilla, placerat orci vel, convallis nisi. Mauris dapibus euismod tempus. Etiam blandit nunc mi, quis tristique dui dapibus accumsan. Maecenas non hendrerit magna. Etiam at faucibus ante. Maecenas a volutpat dolor. In tristique libero id sagittis cursus. Mauris non viverra mi, in placerat purus.",
        "Cool Title 4": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi convallis ante sed lectus ultrices, eget accumsan augue consectetur. Nullam non urna et eros viverra aliquam vitae eu dui. Nulla a mauris fringilla, placerat orci vel, convallis nisi. Mauris dapibus euismod tempus. Etiam blandit nunc mi, quis tristique dui dapibus accumsan. Maecenas non hendrerit magna. Etiam at faucibus ante. Maecenas a volutpat dolor. In tristique libero id sagittis cursus. Mauris non viverra mi, in placerat purus.",
        "Cool Title 5": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi convallis ante sed lectus ultrices, eget accumsan augue consectetur. Nullam non urna et eros viverra aliquam vitae eu dui. Nulla a mauris fringilla, placerat orci vel, convallis nisi. Mauris dapibus euismod tempus. Etiam blandit nunc mi, quis tristique dui dapibus accumsan. Maecenas non hendrerit magna. Etiam at faucibus ante. Maecenas a volutpat dolor. In tristique libero id sagittis cursus. Mauris non viverra mi, in placerat purus."
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


def getBlog (query):
	return {
		query + '1': "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi convallis ante sed lectus ultrices, eget accumsan augue consectetur. Nullam non urna et eros viverra aliquam vitae eu dui. Nulla a mauris fringilla, placerat orci vel, convallis nisi. Mauris dapibus euismod tempus. Etiam blandit nunc mi, quis tristique dui dapibus accumsan. Maecenas non hendrerit magna. Etiam at faucibus ante. Maecenas a volutpat dolor. In tristique libero id sagittis cursus. Mauris non viverra mi, in placerat purus.",
		query + '2': "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi convallis ante sed lectus ultrices, eget accumsan augue consectetur. Nullam non urna et eros viverra aliquam vitae eu dui. Nulla a mauris fringilla, placerat orci vel, convallis nisi. Mauris dapibus euismod tempus. Etiam blandit nunc mi, quis tristique dui dapibus accumsan. Maecenas non hendrerit magna. Etiam at faucibus ante. Maecenas a volutpat dolor. In tristique libero id sagittis cursus. Mauris non viverra mi, in placerat purus.",
		query + '3': "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi convallis ante sed lectus ultrices, eget accumsan augue consectetur. Nullam non urna et eros viverra aliquam vitae eu dui. Nulla a mauris fringilla, placerat orci vel, convallis nisi. Mauris dapibus euismod tempus. Etiam blandit nunc mi, quis tristique dui dapibus accumsan. Maecenas non hendrerit magna. Etiam at faucibus ante. Maecenas a volutpat dolor. In tristique libero id sagittis cursus. Mauris non viverra mi, in placerat purus."
	}

@app.route("/search", methods = ["GET", "POST"])
def search_page():
	if ("searchQuery" in request.args):
		return render_template(fileNames["search"], articles = getBlog(request.args["searchQuery"]))
	# print (request.args["queryString"])
	if "username" in session:
		return render_template(fileNames["search"])
	return render_template(fileNames["login"])

def getMyEntries (userId):
	myEntry = {
		"123" : {"Why cats are cool" : "Cats are the coolest animal"},
		"235" : {"How to become rich" : "Buy money"},
		"344" : {"Grapes are nasty" : "Grapes taste horrible!"}
	}
	return myEntry

@app.route("/edit", methods = ["GET", "POST"])
def edit_page():
	if ("entryId" in request.args):
		idEntryV = request.args["entryId"];
		titleV = list(getMyEntries(121)[idEntryV].keys())[0]
		bodyV = getMyEntries(121)[idEntryV][titleV]
		return render_template(fileNames["editPage"], idEntry = idEntryV, title = titleV, body = bodyV)
	if "username" in session:
		return render_template(fileNames["edit"], entries = getMyEntries(121))
	return render_template(fileNames["login"])

def saveEntry(entryId, newTitle, newBody):
	print(entryId)
	print(newTitle)
	print(newBody)

@app.route("/save", methods = ["POST"])
def save_entry ():
	saveEntry(request.form['entryId'], request.form['title'], request.form['body'])
	return redirect(url_for("edit_page"))

@app.route("/logout")
def logout():
	session.pop("username")
	return redirect(url_for("input_field_page"))

if __name__ == "__main__":
	app.debug = True
	app.run()
