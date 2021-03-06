# MS^2
# Matthew Ming, Sajed Nahian. Stefan Tan, Michelle Tang
# SoftDev1 pd6
# P #00: Da Art of Storytellin'

#part of gdb
import sqlite3   #enable control of an sqlite database
import csv       #facilitates CSV I/O

DB_FILE="weblog.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops

user_count = 0;
blog_count = 0;
entry_count = 0;
def createTables():
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()               #facilitate db ops
    command0 = """
    CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER ,
    username TEXT,
    password TEXT,
    blog_id TEXT)
    """
    command1 = """
    CREATE TABLE IF NOT EXISTS blogs(
    user_id INTEGER,
    blog_id INTEGER,
    blog_title TEXT,
    entry_id TEXT)
    """
    command2 = """
    CREATE TABLE IF NOT EXISTS entries(
    user_id INTEGER,
    blog_id INTEGER,
    entry_id INTEGER,
    entry_title TEXT,
    entry_content TEXT)
    """
    c.execute(command0)
    c.execute(command1)
    c.execute(command2)
    db.commit()
    db.close()
createTables()

def usersDB():
    return "INSERT INTO users(user_id, username, password, blog_id) VALUES( ?, ?, ?, ?)"

def blogsDB():
    return "INSERT INTO blogs (user_id,blog_id,blog_title, entry_id) VALUES( ?, ?, ?, ?)"

def entriesDB():
    return "INSERT INTO entries(user_id, blog_id, entry_id, entry_title, entry_content) VALUES( ?, ?, ?, ?, ?)"

def addUserToDatabase(username,password):
    '''This function checks if the username exists and adds a username and password to the users table'''
    initCount()
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
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
    db.commit()
    db.close()
    return True;

def addBlogToDatabase(userID, blog_title):
    '''This function adds a blog and updates blogid in users table'''
    initCount()
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    global blog_count
    bc = ""
    form_response = (userID, blog_count, blog_title, "")
    c.execute( blogsDB() , form_response)
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
    db.commit()
    db.close()
    print(str(userID) + " " + blog_title)
    print("ADDEDDDDDDDDDDDDDDDDDDDDDDDDDD")
    return True


def addEntryToDatabase(userID, blogID, entry_title, entry_content):
    '''This function adds an entry and updates entryid in blogs table'''
    initCount()
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
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
    db.commit()
    db.close()
    return True

#Login function
def login(username,password):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    '''This function checks if the user and the corresponding password exists in the database'''
    print(username + password)
    search = "SELECT username, password FROM users"
    c.execute(search)
    users = c.fetchall()
    print(users)
    for user in users:
        print(user[0])
        print(user[1])
        if (user[0] == username and user[1] == password):
            print ("LOGIN SUCCESSFUL")
            return True;
    print ("LOGIN DENIED")
    db.commit()
    db.close()
    return False;

#given userid, return five entries that dont belong to you, estalishes feedM
def getRandomEntries(userID):
    '''This function retrieves 5 random entries from the entries table'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    search = "SELECT entry_id, entry_title, entry_content FROM entries WHERE entries.user_id != " + str(userID)
    c.execute(search)
    entries = c.fetchall()
    d = {}
    counter = 0;
    for entry in entries:
        if counter > 4:
            break;
        print (entry[0])
        d[entry[0]]= {}
        d[entry[0]][str(entry[1])] = str(entry[2])
    db.commit()
    db.close()
    return d

# return an entry when given an entryidM
def returnEntry(entryID):
    '''This function returns an entry based on the given entryID'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    search = "SELECT entry_title, entry_content FROM entries WHERE entries.entry_id == " + str(entryID)
    c.execute(search)
    entries = c.fetchall()
    d = {}
    for entry in entries:
        d[str(entry[0])] = str(entry[1])
    print("finished returnentry")
    db.commit()
    db.close()
    return d

## return a nested dionary of YOUR contributions {entry_id : {entrytitle:entry content}}M
def getMyUserEntries(userID):
    '''This function returns all the entries of an userID'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    search = "SELECT entry_id, entry_title, entry_content FROM entries WHERE entries.user_id == " + str(userID)
    c.execute(search)
    entries = c.fetchall()
    d = {}
    for entry in entries:
        d[entry[0]]= {}
        d[entry[0]][str(entry[1])] = str(entry[2])
    print ("finished getmyentries")
    db.commit()
    db.close()
    return d

#returns a list of all of YOUR blog titlesM
def get_my_blog_titles(userID):
    '''This function returns all the blogs of an userID'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    blog_titles = []
    search = "SELECT blog_title FROM blogs WHERE blogs.user_id == " + str(userID)
    c.execute(search)
    blogs = c.fetchall()
    for blog in blogs:
        blog_titles.append(str(blog[0]))
    db.commit()
    db.close()
    return blog_titles

def updateEntry(entryID, title, content):
    '''This function edits an entry in the entries table'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "UPDATE entries SET entry_title = \"{}\", entry_content = \"{}\" WHERE entry_id = {}".format(title, content, entryID)
    c.execute(command)
    db.commit()
    db.close()

def blogID (blogTitle):
    '''This function returns the blogID given the title of the blog'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    search = "SELECT blog_id FROM blogs WHERE blog_title == \"{}\"".format(blogTitle)
    c.execute(search)
    blogID = c.fetchall()
    if (blogID == []):
        return -1
    db.commit()
    db.close()
    return blogID[0][0]

def initCount():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    global user_count, blog_count, entry_count
    search0 = "SELECT user_id FROM users"
    c.execute(search0)
    users = c.fetchall()
    for user in users:
        user_count += 1
    search1 = "SELECT blog_id FROM blogs"
    c.execute(search1)
    blogs = c.fetchall()
    for blog in blogs:
        blog_count += 1
    search2 = "SELECT entry_id FROM entries"
    c.execute(search2)
    entries = c.fetchall()
    for entry in entries:
        entry_count += 1
    db.commit()
    db.close()

def getBlogs(userID, query):
    '''This function returns the blogs of other users'''
    # search = "SELECT blog_id FROM blogs WHERE blog_title == \"{}\"".format(blogTitle)
    initCount()
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    d={}
    user_counter = user_count
    blogs = []
    while (user_counter > -1):
        if (user_counter != userID):
            print(get_my_blog_titles(user_counter))
            blogs += get_my_blog_titles(user_counter)
        user_counter -= 1
    # print("the blogs")
    # print(blogs)
    for blog in blogs:
        if (blog.find(query) != -1):
            d[blogID(blog)] = blog
    # print("finished getBlogs")
    # print("the dictionary")
    # print(d)
    db.commit()
    db.close()
    return d

def getBlogs2 (userId, query):
    '''This function returns a nested dictionary where the entry content has query.'''
    search = "SELECT entry_id, entry_title, entry_content FROM 'entries'"
    initCount()
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute(search)
    result = c.fetchall()
    queriedBlogs = {}
    for val in result:
        if (query in val[2]):
            queriedBlogs[val[0]] = {val[1] : val[2]}
    return queriedBlogs

def checkIfBlogNameInUse(blog_title):
    '''This function checks if the blog_title already exists in the database'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    if (blogID(blog_title) != -1):
        print("blog title is already in use")
        return False
    print("blog title is okay")
    db.commit()
    db.close()
    return True

def getMyId(username):
    '''This function returns the userID given the username'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    search = "SELECT user_id FROM users WHERE username == \"{}\"".format(username)
    c.execute(search)
    userID= c.fetchall()
    db.commit()
    db.close()
    return userID[0][0]

if __name__ == "__main__":
    print(getBlogs2(1, "br"))
