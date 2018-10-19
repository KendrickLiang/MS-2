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


@app.route("/search", methods = ["GET"])
def search_page():
	if "username" in session:
		return render_template(fileNames["search"], articles = getRandomBlogs())
	return render_template(fileNames["login"])

@app.route("/logout")
def logout():
	session.pop("username")
	return redirect(url_for("input_field_page"))

if __name__ == "__main__":
	app.debug = True
	app.run()
