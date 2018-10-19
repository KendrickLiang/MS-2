#part of gdb
import sqlite3   #enable control of an sqlite database
import csv       #facilitates CSV I/O

DB_FILE="weblog.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops

command0 = """
CREATE TABLE users(
user_id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT,
password TEXT,
blog_id TEXT)
"""

command1 = """
CREATE TABLE blogs(
user_id INTEGER,
blog_id INTEGER PRIMARY KEY,
blog_title TEXT,
entry_id TEXT)
"""
command2 = """
CREATE TABLE entries(
user_id INTEGER,
blog_id INTEGER,
entry_id INTEGER PRIMARY KEY,
entry_title TEXT,
entry_content TEXT)
"""
c.execute(command0)
c.execute(command1)
c.execute(command2)

form_response = ('a', 'b', "1,2,3")
c.execute( "INSERT INTO users(username, password, blog_id) VALUES( ?, ? , ?)", form_response )

def addUserToDatabase(username,password):
    search = "SELECT username FROM users"
    c.execute(search)
    users = c.fetchall()
    print(users)
    for user in users:
        if (user[0] == username):
            print ("a user already exists")
            return;
    form_response1 = ( username, password, "");
    c.execute( "INSERT INTO users(username, password, blog_id) VALUES( ?, ? , ?)", form_response1 )

def checkUserInDatabase(username,password):
    search = "SELECT username, password FROM users"
#    search2= "SELECT password FROM users"               #selects IDs
    c.execute(search)
#    c.execute()
    users = c.fetchall()
    for user in users:
        if (user[0] == username and user[1] == password):
            print ("login successful")
    print(users)
def createUser (username,password):
    search = "SELECT username FROM users"



addUserToDatabase("sam", "notsam")
checkUserInDatabase("sam","notsam")
addUserToDatabase("sam", "notsam")


#command3 = "INSERT INTO users VALUES('ab', 'bb', 3)"
#c.execute( "INSERT INTO users(username, password,blog_id) VALUES( ?, ? , ?)", ('ab', 'bc', 2) )

#c.execute(command2)
#c.execute(command3)

db.commit()
db.close()
