import _sqlite3
from flask import session, flash

DB_Location = "DB/User_Data.db"


# Custom context manager for making it easier when accessing database
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

# Function which counts the amount of times an entry appears inside
# of a column in the Users table which can use a condition.
def countEntryInUsers(entry, column1, column2, mode):

    # Mode means does the query need to use = or LIKE, or just to count ALL entries

    if mode == "ALL":
        with openDB(DB_Location) as db:
            db.execute("SELECT COUNT({}) FROM Users".format(column1))
            return db.fetchone()[0]
    else:
        entry = (entry,)
        with openDB(DB_Location) as db:
            db.execute("SELECT COUNT({}) FROM Users WHERE {} {} ?".format(column1, column2, mode), entry)
            return db.fetchone()[0]

# updates an entry in the User table for a user with the current user_id
# uses arrays as parameters so when the program needs to update several
# details it can just iterate across the array to update all of the values.
def updateUserData(entries, columns):

    with openDB(DB_Location) as db:
        for index in range(0, len(entries)):

            entry = (entries[index], session.get("user_id"))
            column = columns[index]
            db.execute("UPDATE Users SET {} = ? WHERE userID = ?".format(column), entry)

            flash(column.capitalize() + " changed successfully to " + entry[0], "success")

# Function which takes a data list with ordered values and inserts it into a new row in the Users table
# to create a new user.
def insertNewUser(data):
    with openDB(DB_Location) as db:
        db.execute(
            "INSERT INTO Users (username, password, forename, surname, email, userID) VALUES (?,?,?,?,?,?)",
            data)


# This function just returns data from the users table to the set conditions which depend of the
# passed in parameters.
def selectUserDataFromDB(entry, column1, column2, mode):
    entry = (entry,)
    with openDB(DB_Location) as db:
        db.execute("SELECT {} FROM Users WHERE {} {} ?".format(column1, column2, mode), entry)
        return db.fetchone()[0]


#  This function returns all of a users data corresponding to the userID in the Users table
def selectAllUserData(userID):
    userID = (userID,)
    with openDB(DB_Location) as db:
        db.execute("SELECT username, forename, surname, email FROM Users WHERE userID = ?", userID)
        return db.fetchone()

# This function returns all of the cards in the table Cards which belong to a user with the userID passed in
# as a parameter.
def selectUserCards(userID):
    userID = (userID,)

    with openDB(DB_Location) as db:
        db.execute("SELECT question, answer, cardID FROM Cards WHERE userID = ?", userID)
        return db.fetchall()


# This function returns one card with a matching cardID
def selectThisCard(cardID):
    cardID = (cardID,)

    with openDB(DB_Location) as db:
        db.execute("SELECT question, answer, userID FROM Cards WHERE cardID = ?", cardID)
        return db.fetchone()


# This function updates the question and answer of a card with the corresponding passed in cardID.
def updateUserCard(question, answer, cardID):
    data = (question, answer, cardID)

    with openDB(DB_Location) as db:
        db.execute("UPDATE Cards SET question = ?, answer = ? WHERE cardID = ?", data)


# This function counts how many cards a user has by counting how many cards have a matching userID.
def countUserCards(userID):
    userID = (userID,)

    with openDB(DB_Location) as db:
        db.execute("SELECT COUNT(cardID) FROM Cards WHERE userID = ?", userID)
        return db.fetchone()[0]


# This function creates the DB and Tables if they do not exist.
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

        db.execute('''

        CREATE TABLE IF NOT EXISTS Cards(
        cardID INTEGER ,
        question TEXT,
        answer TEXT,
        userID INTEGER 

                )''')

        # Test Data


        db.execute("INSERT INTO Cards (cardID, question, answer, userID) VALUES (1, 'User 1s question1', 'User 1s answer1', 1)")
        db.execute("INSERT INTO Cards (cardID, question, answer, userID) VALUES (2, 'User 1s question2', 'User 1s answer2', 1)")
        db.execute("INSERT INTO Cards (cardID, question, answer, userID) VALUES (3, 'User 1s question3', 'User 1s answer3', 1)")

        db.execute("INSERT INTO Cards (cardID, question, answer, userID) VALUES (4, 'User 2s question1', 'User 2s answer1', 2)")
        db.execute("INSERT INTO Cards (cardID, question, answer, userID) VALUES (5, 'User 2s question2', 'User 2s answer2', 2)")
        db.execute("INSERT INTO Cards (cardID, question, answer, userID) VALUES (6, 'User 2s question3', 'User 2s answer3', 2)")
