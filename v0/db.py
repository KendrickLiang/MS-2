import sqlite3   #enable control of an sqlite database
import csv       #facilitates CSV I/O

DB_FILE="weblog.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops

command = "CREATE TABLE {}({1},{2},{3})".format\
("users", "user_id INTEGER PRIMARY KEY AUTOINCREMENT", "username TEXT", "password TEXT", "blog_id INTEGER")
c.execute(command)
command2 = "INSERT INTO users VALUES(0, 'a', 'b', 2)"
c.execute(command2)

db.commit()
db.close()
