import _sqlite3
from flask import session, flash
DB_Location = "DB/User_Data.db"

class openDB():
    def __init__(self, DBname):
        self.DBname = DBname
        self.connection = _sqlite3.connect(DBname)
        self.db = self.connection.cursor()

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()
        self.db.close()
        print(self.db.rowcount)


def countEntry(entry, column1, column2, mode):
    # Mode means does the query need to use = or LIKE, or just to count ALL entries
    # Created this function to minimise the amount of SQL statements dotted around everywhere

    if mode == "ALL":
        with openDB(DB_Location) as db:
            db.execute("SELECT COUNT({}) FROM Users".format(column1))
            return db.fetchone()[0]
    else:
        entry = (entry,)
        with openDB(DB_Location) as db:
            db.execute("SELECT COUNT({}) FROM Users WHERE {} {} ?".format(column1, column2, mode), entry)
            return db.fetchone()[0]


def updateData(entries, columns):
    with openDB(DB_Location) as db:
        for index in range(0, len(entries)):
            entry = (entries[index], session.get("user_id"))
            column = columns[index]

            db.execute("UPDATE Users SET {} = ? WHERE userID = ?".format(column), entry)

            flash(column.capitalize() + " changed successfully to " + entry[0], "success")




def insertNewUser(data):
    with openDB(DB_Location) as db:
        db.execute(
            "INSERT INTO Users (username, password, forename, surname, email, userID) VALUES (?,?,?,?,?,?)",
            data)


def selectDataFromDB(entry, column1, column2, mode):
    entry = (entry,)
    with openDB(DB_Location) as db:
        db.execute("SELECT {} FROM Users WHERE {} {} ?".format(column1, column2, mode), entry)
        return db.fetchone()[0]


def selectAllUserData(userID):

    userID = (userID,)
    with openDB(DB_Location) as db:
        db.execute("SELECT username, forename, surname, email FROM Users WHERE userID = ?", userID)
        user = db.fetchone()



def innitializeUser_DB():
    with openDB("DB/User_Data.db") as db:
        db.execute('''
        
        CREATE TABLE IF NOT EXISTS Users(
        username TEXT,
        password TEXT,
        forename TEXT,
        surname TEXT,
        email TEXT,
        userID INTEGER
        
        )''')

