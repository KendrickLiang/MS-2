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


def hardCode():
    form_response = ('a_username', 'a_password', "1")
    c.execute( users(), form_response )
    form_response = ('1', '1', 'Cats', "1")
    c.execute( blogs(), form_response )
    form_response = ('1', '1', '1', 'Cats', 'I like them.')
    c.execute( "INSERT INTO entries(user_id, blog_id, entry_id, entry_title, entry_content) VALUES( ?, ?, ?, ?, ?)", form_response )
    print ("!!finished inserting set values!!")


def addUserToDatabase(username,password):
    search = "SELECT username FROM users"
    c.execute(search)
    users = c.fetchall()
    print(users)
    for user in users:
        if (user[0] == username):
            print ("a user already exists")
            return False;
    form_response1 = ( username, password, "");
    c.execute( "INSERT INTO users(username, password, blog_id) VALUES( ?, ? , ?)", form_response1 )

def loginDatabase(username,password):
    search = "SELECT username, password FROM users"
    c.execute(search)
    users = c.fetchall()
    for user in users:
        if (user[0] == username and user[1] == password):
            print ("login successful")
    print(users)

def createNewBlog( userID, title ):
    form_response1 = ( username, password, "");
    c.execute( blogs(), form_response1 )



def users():
    return "INSERT INTO users(username, password, blog_id) VALUES( ?, ?, ?)"

def blogs():
    return "INSERT INTO blogs (user_id,blog_id,blog_title, entry_id) VALUES( ?, ?, ?, ?)"

def
# def createUser (username,password):
#     search = "SELECT username FROM users"
#     c.execute(search)
#     users= c.fetchall()
#     for user in users:
#         if (user[0] == username):
#             print ("user already exists")
hardCode()
addUserToDatabase("sam", "notsam")
loginDatabase("sam","notsam")
addUserToDatabase("sam", "notsam")

#done #  check_username_in_db (username) returns bool
# done # save_user_signup (usernbame, password) return void
# getRandomBlogs () returns dictionary of random blogs emntries where key is title of entry and value is cotent of entry_id
# def getBlog (query) returns dictionary (same as getRandomBlogs) where title contains the query
# getMyEntries (userID) returns dictionary dictionary (look at app.py to see what it returns)
# saveEntry (entryID, newTitle, newBody) modifies the entry with the new title and new newBody
# checkIFBlogNameInUse (name)
# def get_my_blog_titles take look at app.def foo():
# createNEwBlog (name)
# getMyId(username)
# i love this keyboard it is so fun to type on. It feels soooo good why does this keyboard feel so

 #    doc = "The  property."
 #    def fget(self):
 #        return self._
 #    def fset(self, value):
 #        self._ = value
 #    def fdel(self):
 #        del self._
 #    return locals()
 # = property(**())

#command3 = "INSERT INTO users VALUES('ab', 'bb', 3)"
#c.execute( "INSERT INTO users(username, password,blog_id) VALUES( ?, ? , ?)", ('ab', 'bc', 2) )

#c.execute(command2)
#c.execute(command3)

db.commit()
db.close()
