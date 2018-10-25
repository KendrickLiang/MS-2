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
    c.execute( usersDB(), form_response )
    form_response = ('B_username', 'B_password', "2")
    c.execute( usersDB(), form_response )
    form_response = ('1', '1', 'Cats', "1")
    c.execute( blogsDB(), form_response )
    form_response = ('0', '1', '1', 'Cats', 'Yay.')
    c.execute( entriesDB(), form_response )
    form_response = ('1', '1', '2', 'Dogs', 'Yay.')
    c.execute( entriesDB(), form_response )
    form_response = ('1', '1', '3', 'Birds', 'Yay.')
    c.execute( entriesDB(), form_response )
    form_response = ('1', '1', '4', 'Fish', 'Yay.')
    c.execute( entriesDB(), form_response )
    form_response = ('1', '1', '5', 'Ants', 'Yay.')
    c.execute( entriesDB(), form_response )
    form_response = ('1', '1', '6', 'Ducks', 'Yay.')
    c.execute( entriesDB(), form_response )
    form_response = ('1', '1', '7', 'Geese', 'Yay.')
    c.execute( entriesDB(), form_response )
    form_response = ('1', '1', '8', 'Rats', 'Yay.')
    c.execute( entriesDB(), form_response )
    print ("!!finished inserting set values!!")

def usersDB():
    return "INSERT INTO users(username, password, blog_id) VALUES( ?, ?, ?)"

def blogsDB():
    return "INSERT INTO blogs (user_id,blog_id,blog_title, entry_id) VALUES( ?, ?, ?, ?)"

def entriesDB():
    return "INSERT INTO entries(user_id, blog_id, entry_id, entry_title, entry_content) VALUES( ?, ?, ?, ?, ?)"

hardCode()

def addUserToDatabase(username,password):
    search = "SELECT username FROM users"
    c.execute(search)
    users = c.fetchall()
    print(users)
    for user in users:
        if (user[0] == username):
            print ("a user already exists")
            return False;
    form_response = (username, password, "")
    c.execute( usersDB() , form_response )
    return True;

def loginDatabase(username,password):
    search = "SELECT username, password FROM users"
    c.execute(search)
    users = c.fetchall()
    for user in users:
        if (user[0] == username and user[1] == password):
            print ("login successful")
            print(user)
            return True;
    print ("login denied")
    return False;

#given userid, return five entries
def getRandomEntries(userID):
    search = "SELECT entry_id, entry_title, entry_content FROM entries WHERE entries.user_id != " + str(userID)
    c.execute(search)
    entries = c.fetchall()
    dict = {}
    counter = 0;
    for entry in entries:
        if counter > 4:
            break;
        print (entry[0])
        dict[entry[0]]= {}
        dict[entry[0]][str(entry[1])] = str(entry[2])
        #counter += 1
    print dict
    print ("shmur")

getRandomEntries(0)

def returnEntry(entryID):
    print("testing return entry")
    search = "SELECT username, entry_title, entry_content FROM users, entries WHERE entries.entry_id == " + str(entryID) + " AND users.user_id == entries.user_id"
    c.execute(search)
    entry = c.fetchall()
    print ("THIS IS THE ENTRY")
    # will give back user, title of entry, and content of entry
    print entry

returnEntry(3)

def getMyEntries(userID):
    search = "SELECT entry_title, entry_content FROM entries WHERE entries.user_id == " + str(userID)
    c.execute(search)
    entries = c.fetchall()
    dict = {}
    for entry in entries:
        dict[str(entry[0])] = str(entry[1])
    print dict
    print ("testing getmyentries")

getMyEntries(1)

def saveEntry(entryID, newTitle, newBody):
    print(newTitle)
    print(str(newTitle))
    search = "UPDATE entries SET entry_title =" + ''' newTitle''' + "WHERE entry_id == " + str(entryID)
    print (repr(search))
    c.execute(search)
    print ("save entry")

#try this out: cursor.execute ( ''' update books set price = ? where id = ?''', (newPrice, book_id)
saveEntry(1, 'newDog', "newYay")

you a keyword, i will return a title and a content and th eid.
#     form_response1 = ( username, password, "");
#     c.execute( blogs(), form_response1 )
#
# in velocity:
# if it is above x axis, moving to the right
# if it is below the x axis, moving to the leftself.
# when determining distance,
# def getBlog (query) returns dictionary (same as getRandomBlogs) where title contains the query
# getMyEntries (userID) returns dictionary dictionary (look at app.py to see what it returns)
# saveEntry (entryID, newTitle, newBody) modifies the entry with the new title and new newBody
# checkIFBlogNameInUse (name)
# def get_my_blog_titles take look at app.def foo():
# createNEwBlog (name)
# getMyId(username)


# def createUser (username,password):
#     search = "SELECT username FROM users"
#     c.execute(search)
#     users= c.fetchall()
#     for user in users:
#         if (user[0] == username):
#             print ("user already exists")
addUserToDatabase("sam", "notsam")
loginDatabase("sam","notsam")

#done #  check_username_in_db (username) returns bool
#done # save_user_signup (usernbame, password) return void
#done # getRandomEntries () returns dictionary of random blogs entries where key is title of entry and value is cotent of entry_id


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
