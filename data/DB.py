from flask import session, flash, current_app
from flask_sqlalchemy import SQLAlchemy


# Custom context manager for making it easier when accessing database
# https://pythonbasics.org/flask-sqlalchemy/
class openDB():
    def __init__(self):
        self.session = SQLAlchemy(current_app)

    def __enter__(self):
        return self.session.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.session.commit()


# Initialization of DB using flask sqlalchemy https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/
def initializeDB():
    
    current_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////DB/DB.session'
    current_app.config['SQLALCHEMY_ECHO'] = True #For Debugging
    
    session = SQLAlchemy(current_app)

    class Users(session.Model):
        username = session.Column("username", session.String)
        password = session.Column("password", session.String)
        forename = session.Column("forname", session.String)
        surname = session.Column("surname", session.String)
        email = session.Column("email", session.String)
        userID = session.Column("userID", session.Integer, primary_key=True, autoincrement=True)
        

    class Cards(session.Model):
        question = session.Column("question", session.String)
        answer = session.Column("answer", session.String)
        cardID = session.Column("cardID", session.Integer, primary_key=True, autoincrement=True)
        userID = session.Column(session.Integer, session.ForeignKey("user.userID"), nullable=False)
        users = session.relationship("Users", backref="user", lazy=True)


    session.create_all()



# Function which counts the amount of times an entry appears inside
# of a column in the Users table which can use a condition.
def countEntryInUsers(entry, column1, column2, mode):
    # Mode means does the query need to use = or LIKE, or just to count ALL entries

    if mode == "ALL":
        with openDB(DB_Location) as session:
            session.execute(text("SELECT COUNT({}) FROM Users".format(column1)))
            return session.fetchone()[0]
    else:
        entry = (entry,)
        with openDB(DB_Location) as session:
            session.execute(text("SELECT COUNT({}) FROM Users WHERE {} {} ?".format(column1, column2, mode), entry))
            return session.fetchone()[0]


# updates an entry in the User table for a user with the current user_id
# uses arrays as parameters so when the program needs to update several
# details it can just iterate across the array to update all of the values.
def updateUserData(attribute, user):
    with openDB(DB_Location) as session:
        user = session


# Function which takes a data list with ordered values and inserts it into a new row in the Users table
# to create a new user.
def insertNewUser(user):

    with openDB(DB_Location) as session:
        session.add(user)

        


# This function just returns data from the users table to the set conditions which depend of the
# passed in parameters.
def selectUserDataFromDB(entry, column1, column2, mode):
    entry = (entry,)
    with openDB(DB_Location) as session:
        session.execute(text("SELECT {} FROM Users WHERE {} {} ?".format(column1, column2, mode), entry))
        return session.fetchone()[0]


#  This function returns all of a users data corresponding to the userID in the Users table
def selectAllUserData(userID):
    userID = (userID,)
    with openDB(DB_Location) as session:
        session.execute(text("SELECT username, forename, surname, email FROM Users WHERE userID = ?", userID))
        return session.fetchone()


# Deletes user from Users table and all cards with corresponding userID
def deleteUser(userID):
    userID = (userID,)
    with openDB(DB_Location) as session:
        session.execute(text("DELETE FROM Cards WHERE userID = ?", userID))
        session.execute(text("DELETE FROM Users WHERE userID = ?", userID))


# This function returns all of the cards in the table Cards which belong to a user with the userID passed in
# as a parameter.
def selectUserCards(userID):
    userID = (userID,)

    with openDB(DB_Location) as session:
        session.execute(text("SELECT question, answer, cardID FROM Cards WHERE userID = ?", userID))
        return session.fetchall()


# This function returns one card with a matching cardID
def selectThisCard(cardID):
    cardID = (cardID,)

    with openDB(DB_Location) as session:
        session.execute(text("SELECT question, answer, userID FROM Cards WHERE cardID = ?", cardID))
        return session.fetchone()


# This function updates the question and answer of a card with the corresponding passed in cardID.
def updateUserCard(question, answer, cardID):
    data = (question, answer, cardID)

    with openDB(DB_Location) as session:
        session.execute(text("UPDATE Cards SET question = ?, answer = ? WHERE cardID = ?", data))

# This function creates a card in the database
def createCard(question, answer, userID):

    data = (question, answer, userID)

    with openDB(DB_Location) as session:
        session.execute(text("INSERT INTO Cards (question, answer, userID) VALUES (?,?,?)", data))


# This function deletes card with corresponding cardID
def deleteCard(cardID):

    cardID = (cardID,)

    with openDB(DB_Location) as session:

        session.execute(text("DELETE FROM Cards WHERE cardID = ?", cardID))



# This function counts how many cards a user has by counting how many cards have a matching userID.
def countUserCards(userID):
    userID = (userID,)

    with openDB(DB_Location) as session:
        session.execute(text("SELECT COUNT(cardID) FROM Cards WHERE userID = ?", userID))
        return session.fetchone()[0]



