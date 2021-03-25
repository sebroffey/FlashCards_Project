from flask import session, flash
from flask_sqlalchemy import SQLAlchemy






# Custom context manager for making it easier when accessing database
# https://pythonbasics.org/flask-sqlalchemy/
class openDB():
    def __init__(self, DBname):
        self.db = SQLAlchemy(app)
        
        self.creation = False

        if not engine.dialect.has_table(engine, "user_account"):
            innitializeUserTable(self.metadata)
            creation = True
        if not engine.dialect.has_table(engine, "user_cards"):
            innitializeCardsTable(self.metadata)    
            creation = True
        if creation:
            self.metadata.create_all(self.engine)
    def __enter__(self):
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        # self.db.close()
        # print(self.db.rowcount)


def initializeDB(app):
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////DB/DB.db'
    app.config['SQLALCHEMY_ECHO'] = True #For Debugging
    
    db = SQLAlchemy(app)

    class Users(db.Model):
        username = db.Column("username", db.String)
        password = db.Column("password", db.String)
        forename = db.Column("forname", db.String)
        surname = db.Column("surname", db.String)
        email = db.Column("email", db.String)
        userID = db.Column("userID", db.Integer, primary_key=True, autoincrement=True)

        def __repr__(self):
            return "<User %r>" % self.username


    class Cards(db.Model):
        question = db.Column("question", db.String)
        answer = db.Column("answer", db.String)
        cardID = db.Column("cardID", db.Integer, primary_key=True, autoincrement=True)
        userID = db.Column("userID", db.Integer, autoincrement=True)

        def __repr__(self):
            return "<Card %r>" % self.cardID
      
      
    db.create_all()



def innitializeCardsTable(metadata:MetaData):
    Cards = Table(
        "user_cards",
        db.metadata,
        Column("question", String)
        Column("answer", String)
        Column("userID", Integer, ForeignKey("user_account.userID"), nullable=False)
        Column("cardID", Integer, primary_key=True, autoincrement=True)            
    )
    metadata.create_all()



# Function which counts the amount of times an entry appears inside
# of a column in the Users table which can use a condition.
def countEntryInUsers(entry, column1, column2, mode):
    # Mode means does the query need to use = or LIKE, or just to count ALL entries

    if mode == "ALL":
        with openDB(DB_Location) as db:
            db.execute(text("SELECT COUNT({}) FROM Users".format(column1)))
            return db.fetchone()[0]
    else:
        entry = (entry,)
        with openDB(DB_Location) as db:
            db.execute(text("SELECT COUNT({}) FROM Users WHERE {} {} ?".format(column1, column2, mode), entry))
            return db.fetchone()[0]


# updates an entry in the User table for a user with the current user_id
# uses arrays as parameters so when the program needs to update several
# details it can just iterate across the array to update all of the values.
def updateUserData(entries, columns):
    with openDB(DB_Location) as db:
        for index in range(0, len(entries)):

            entry = (entries[index], session.get("user_id"))
            column = columns[index]
            db.execute(text("UPDATE Users SET {} = ? WHERE userID = ?".format(column), entry))

            if column != "password":
                flash(column.capitalize() + " changed successfully to " + entry[0], "success")


# Function which takes a data list with ordered values and inserts it into a new row in the Users table
# to create a new user.
def insertNewUser(data):
    
    stmt = insert(User).values(username=data[0], password=data[1], forename=data[2], surname=data[3], email=data[4])
    with openDB(DB_Location) as db:
        result = db.execute(stmt)

        


# This function just returns data from the users table to the set conditions which depend of the
# passed in parameters.
def selectUserDataFromDB(entry, column1, column2, mode):
    entry = (entry,)
    with openDB(DB_Location) as db:
        db.execute(text("SELECT {} FROM Users WHERE {} {} ?".format(column1, column2, mode), entry))
        return db.fetchone()[0]


#  This function returns all of a users data corresponding to the userID in the Users table
def selectAllUserData(userID):
    userID = (userID,)
    with openDB(DB_Location) as db:
        db.execute(text("SELECT username, forename, surname, email FROM Users WHERE userID = ?", userID))
        return db.fetchone()


# Deletes user from Users table and all cards with corresponding userID
def deleteUser(userID):
    userID = (userID,)
    with openDB(DB_Location) as db:
        db.execute(text("DELETE FROM Cards WHERE userID = ?", userID))
        db.execute(text("DELETE FROM Users WHERE userID = ?", userID))


# This function returns all of the cards in the table Cards which belong to a user with the userID passed in
# as a parameter.
def selectUserCards(userID):
    userID = (userID,)

    with openDB(DB_Location) as db:
        db.execute(text("SELECT question, answer, cardID FROM Cards WHERE userID = ?", userID))
        return db.fetchall()


# This function returns one card with a matching cardID
def selectThisCard(cardID):
    cardID = (cardID,)

    with openDB(DB_Location) as db:
        db.execute(text("SELECT question, answer, userID FROM Cards WHERE cardID = ?", cardID))
        return db.fetchone()


# This function updates the question and answer of a card with the corresponding passed in cardID.
def updateUserCard(question, answer, cardID):
    data = (question, answer, cardID)

    with openDB(DB_Location) as db:
        db.execute(text("UPDATE Cards SET question = ?, answer = ? WHERE cardID = ?", data))

# This function creates a card in the database
def createCard(question, answer, userID):

    data = (question, answer, userID)

    with openDB(DB_Location) as db:
        db.execute(text("INSERT INTO Cards (question, answer, userID) VALUES (?,?,?)", data))


# This function deletes card with corresponding cardID
def deleteCard(cardID):

    cardID = (cardID,)

    with openDB(DB_Location) as db:

        db.execute(text("DELETE FROM Cards WHERE cardID = ?", cardID))



# This function counts how many cards a user has by counting how many cards have a matching userID.
def countUserCards(userID):
    userID = (userID,)

    with openDB(DB_Location) as db:
        db.execute(text("SELECT COUNT(cardID) FROM Cards WHERE userID = ?", userID))
        return db.fetchone()[0]


# This function creates the DB and Tables if they do not exist.

        # Test Data


        # db.execute(text("INSERT INTO Cards (question, answer, userID) VALUES ('User 1s question2', 'User 1s answer2', 1)")
        # db.execute(text("INSERT INTO Cards (question, answer, userID) VALUES ('User 1s question3', 'User 1s answer3', 1)")
        #
        # db.execute(text("INSERT INTO Cards (question, answer, userID) VALUES ('User 2s question1', 'User 2s answer1', 2)")
        # db.execute(text("INSERT INTO Cards (question, answer, userID) VALUES ('User 2s question2', 'User 2s answer2', 2)")
        # db.execute(text("INSERT INTO Cards (question, answer, userID) VALUES ('User 2s question3', 'User 2s answer3', 2)")
