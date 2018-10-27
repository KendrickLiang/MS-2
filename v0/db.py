#part of gdb
import sqlite3   #enable control of an sqlite database
import csv       #facilitates CSV I/O

DB_FILE="weblog.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops

user_count = 0;
blog_count = 0;
entry_count = 0;

command0 = """
CREATE TABLE users(
user_id INTEGER PRIMARY KEY,
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

def addUserToDatabase(username,password):
    global user_count
    search = "SELECT username FROM users"
    c.execute(search)
    users = c.fetchall()
    for user in users:
        if (user[0] == username):
            print ("a user already exists")
            return False;
    form_response = (user_count, username, password, "")
    c.execute( usersDB() , form_response )
    user_count += 1
    print("finished addUserToDatabase")
    return True;

def addBlogToDatabase(userID, blog_title):
    global blog_count
    bc = ""
    form_response = (userID, blog_count, blog_title, "")
    c.execute( blogsDB(), form_response)
    #updates user
    search = "SELECT blog_id FROM users WHERE user_id == " + str(userID)
    c.execute(search)
    blog_counts = c.fetchall()
    for b in blog_counts:
        bc += str(b[0])
    bc += str(blog_count)
    command = "UPDATE users SET blog_id = \"{}\" WHERE user_id = {}".format(bc,userID)
    c.execute (command)
    blog_count += 1
    print ("finished addBlogToDatabase")
    return True

def addEntryToDatabase(userID, blogID, entry_title, entry_content):
    global entry_count
    ec = ""
    form_response = (userID, blogID, entry_count, entry_title, entry_content)
    c.execute( entriesDB(), form_response)
    #updates blogs
    search = "SELECT entry_id FROM blogs WHERE blog_id == " + str(blogID)
    c.execute(search)
    blog_counts = c.fetchall()
    for e in blog_counts:
        ec += str(e[0])
    ec += str(entry_count)
    command = "UPDATE blogs SET entry_id = \"{}\" WHERE blog_id = {}".format(ec,blogID)
    c.execute (command)
    entry_count += 1
    print ("finished addEntryToDatabase")
    return True


def hardCode():
    addUserToDatabase ("a_username", "a_password")
    addUserToDatabase ("b_username", "b_password")
    addUserToDatabase ("c_username", "b_password")

    addBlogToDatabase ( 0 , "BlogOnCats")
    addBlogToDatabase ( 0 , "BlogOnDats")
    addBlogToDatabase ( 1 , "BlogOnEats")
    addBlogToDatabase ( 1 , "BlogOnFats")
    addBlogToDatabase ( 2 , "BlogOnGats")
    addBlogToDatabase ( 2 , "BlogOnHats")

    addEntryToDatabase ( 0 , 1, "Cat1", "Cats are cool.")
    addEntryToDatabase ( 0 , 1, "Cat2", "Cats are so cool.")
    addEntryToDatabase ( 0 , 1, "Cat3", "Cats are so so cool.")
    addEntryToDatabase ( 1 , 3, "Cat4", "Cats are cool.")
    addEntryToDatabase ( 1 , 3, "Cat5", "Cats are so cool.")
    addEntryToDatabase ( 2 , 3, "Cat6", "Cats are so so cool.")


def usersDB():
    return "INSERT INTO users(user_id, username, password, blog_id) VALUES( ?, ?, ?, ?)"
def blogsDB():
    return "INSERT INTO blogs (user_id,blog_id,blog_title, entry_id) VALUES( ?, ?, ?, ?)"
def entriesDB():
    return "INSERT INTO entries(user_id, blog_id, entry_id, entry_title, entry_content) VALUES( ?, ?, ?, ?, ?)"

hardCode()

def loginDatabase(username,password):
    search = "SELECT username, password FROM users"
    c.execute(search)
    users = c.fetchall()
    for user in users:
        if (user[0] == username and user[1] == password):
            print ("LOGIN SUCCESSFUL")
            return True;
    print ("LOGIN DENIED")
    return False;

#given userid, return five entries that dont belong to you, estalishes feed
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
    print dict

# return an entry when given an entryid
def returnEntry(entryID):
    search = "SELECT entry_title, entry_content FROM entries WHERE entries.entry_id == " + str(entryID)
    c.execute(search)
    entries = c.fetchall()
    dict = {}
    for entry in entries:
        dict[str(entry[0])] = str(entry[1])
    print("finished returnentry")
    return dict

print(returnEntry(0))

## return a nested dictionary of YOUR contributions {entry_id : {entrytitle:entry content}}
def getMyUserEntries(userID):
    search = "SELECT entry_id, entry_title, entry_content FROM entries WHERE entries.user_id == " + str(userID)
    c.execute(search)
    entries = c.fetchall()
    dict = {}
    for entry in entries:
        dict[entry[0]]= {}
        dict[entry[0]][str(entry[1])] = str(entry[2])
    print ("finished getmyentries")
    return dict
print(getMyUserEntries(0))

#returns a list of all of YOUR blog titles
def get_my_blog_titles(userID):
    blog_titles = []
    search = "SELECT blog_title FROM blogs WHERE blogs.user_id == " + str(userID)
    c.execute(search)
    blogs = c.fetchall()
    for blog in blogs:
        blog_titles.append(str(blog[0]))
    #print("finished get_my_blog_titles")
    return blog_titles

print(get_my_blog_titles(0))

def updateEntry(entryID, title, content):
    command = "UPDATE entries SET entry_title = \"{}\", entry_content = \"{}\" WHERE entry_id = {}".format(title, content, entryID)
    c.execute(command)

updateEntry(0, "Newtitle", "newcontent")

def blogID (blogTitle):
    search = "SELECT blog_id FROM blogs WHERE blog_title == \"{}\"".format(blogTitle)
    c.execute(search)
    blogID = c.fetchall()
    if (blogID == []):
        return -1
    return blogID[0][0]

# returns a nested dictionary {blogID: blogTitle} GET BLOGS TITLES THAT ARENT YOUR OWN
def getBlogs(userID, query):
    dict={}
    user_counter = user_count
    blogs = []
    while (user_counter > 0):
        if (user_counter != userID):
            blogs += get_my_blog_titles(user_counter)
        user_counter -= 1
    for blog in blogs:
        if (blog.find(query) != -1):
            dict[blogID(blog)] = blog
    print("finished getBlogs")
    print(dict)
    return blogs

print (getBlogs(3, "On"))

def checkIfBlogNameInUse(blog_title):
    if (blogID(blog_title) != -1):
        print("blog title is already in use")
        return False
    print("blog title is okay")
    return True

def getMyId(username):
    search = "SELECT user_id FROM users WHERE username == \"{}\"".format(username)
    c.execute(search)
    userID= c.fetchall()
    return userID[0][0]
print(getMyId("b_username"))


db.commit()
db.close()
