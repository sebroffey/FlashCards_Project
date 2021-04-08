from flask import session, flash, current_app
from flask_sqlalchemy import SQLAlchemy

# Initialization of DB using flask sqlalchemy https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/


    
current_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////DB/DB.session'
current_app.config['SQLALCHEMY_ECHO'] = True #For Debugging

session = SQLAlchemy(current_app)

class User(session.Model):
    id = session.Column("userID", session.Integer, primary_key=True, autoincrement=True)
    username = session.Column("username", session.String)
    password = session.Column("password", session.String)
    forename = session.Column("forname", session.String)
    surname = session.Column("surname", session.String)
    email = session.Column("email", session.String)

    cards = session.relationship("cards", backref="user", lazy=True)

    def __init__(user):
        
        if user.username:
            self.username = user.username
        if user.password:
            self.password = user.password
        if user.forename:
            self.forename = user.forename
        if user.surname:
            self.surname = user.surname
        if user.email:
            self.email = user.email
        
        if user.id:
            self.id = user.id
    

class Card(session.Model):
    id = session.Column("cardID", session.Integer, primary_key=True, autoincrement=True)
    question = session.Column("question", session.String)
    answer = session.Column("answer", session.String)
    user_id = session.Column(session.Integer, session.ForeignKey("user.id"), nullable=False)
    
    def __init__(card):
        
            if card.question:
                self.question = card.question
            if card.answer:
                self.answer = card.answer
            if card.userID:
                self.userID = card.userID

            if card.id:
                self.id = card.id

session.create_all()

# Custom context manager for making it easier when accessing database
# https://pythonbasics.org/flask-sqlalchemy/


class openDB():
    def __init__(self):
        self.session = SQLAlchemy(current_app)

    def __enter__(self):
        return self.session.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.session.commit()



def commit_changes(user):
    user_id = user.id

    with openDB(DB_Location) as session:

        DB_user = User.query.filter_by(id=user_id).first()
        if DB_user:
            DB_user.username = user.username
            DB_user.forename = user.forename
            DB_user.surname = user.surname
            DB_user.email = user.email


def update_user_password(user):
    user_id = user.id

    with openDB(DB_Location) as session:

        DB_user = User.query.filter_by(id=user_id).first()

        if DB_user:
            DB_user.password = user.password()

def insert_new_user(user):
    DB_user = User(user)
    with openDB(DB_Location) as session:
        
        session.add(DB_user)
    return user.id


def load_user(user):
    user_id = user.id

    with openDB(DB_Location) as session:
        DB_user = User.query.filter_by(id=user_id).first()

    return DB_user

def return_user_cards(user_id):
    
    with openDB(DB_Location) as session:
        cards = Cards.query.filter_by(user_id=user_id).all()

    return cards

def count_cards(user):
    
    with openDB(DB_Location) as session:
        cards = Card.query.filter_by(user_id=user.id).all()
    return len(cards)



def delete_user(user):
    user_id = user.id
    with openDB(DB_Location) as session:
        DB_user = User.query.filter_by(id=user_id).first()
        session.delete(DB_user)






def load_card(card):
    card_id = card.id
    with openDB(DB_Location) as session:
        DB_card = Card.query.filter_by(id = card_id).first()
    return DB_card

#Updates card question and answer
def update_card(card):
    card_id = card.id
    with openDB(DB_Location) as session:
        DB_card = Card.query.filter_by(id = card_id).first()
        DB_card.question = card.question
        DB_card.answer = card.answer

def insert_new_card(card):
    DB_card = Card(card)
    with openDB(DB_Location) as session:
        session.add(DB_card)
    return card.id

def delete_card(card):
    card_id = card.id
    with openDB(DB_Location) as session:
        DB_card = Card.query.filter_by(id = card_id).first()
        session.delete(DB_card)



def return_userID_with_email(user_email):
    with openDB(DB_Location) as session:
        DB_user = User.query.filter_by(email = user_email).first()
    
    return DB_user

def return_userID_with_username(user_username):
    with openDB(DB_Location) as session:
        DB_user = User.query.filter_by(username = user_username).first()
    
    return DB_user

def check_unique_username(user):
    with openDB(DB_Location) as sessopm:
        users = User.query.filter_by(username=user.username).all()
        if not len(users):
            return True
        else:
            return False

def check_unique_email(user):
    with openDB(DB_Location) as session:
        users = User.query.filter_by(email=user.email).all()
        if not len(users):
            return True
        else:
            return False 
   
# #DONE
# # Function which counts the amount of times an entry appears inside
# # of a column in the Users table which can use a condition.
# def countEntryInUsers(entry, column1, column2, mode):
#     # Mode means does the query need to use = or LIKE, or just to count ALL entries

#     if mode == "ALL":
#         with openDB(DB_Location) as session:
#             session.execute(text("SELECT COUNT({}) FROM Users".format(column1)))
#             return session.fetchone()[0]
#     else:
#         entry = (entry,)
#         with openDB(DB_Location) as session:
#             session.execute(text("SELECT COUNT({}) FROM Users WHERE {} {} ?".format(column1, column2, mode), entry))
#             return session.fetchone()[0]


# # updates an entry in the User table for a user with the current user_id
# # uses arrays as parameters so when the program needs to update several
# # details it can just iterate across the array to update all of the values.


            

        

            






# # Function which takes a data list with ordered values and inserts it into a new row in the Users table
# # to create a new user.

        

        

# #DONE
# # This function just returns data from the users table to the set conditions which depend of the
# # passed in parameters.
# def selectUserDataFromDB(entry, column1, column2, mode):
#     entry = (entry,)
#     with openDB(DB_Location) as session:
#         session.execute(text("SELECT {} FROM Users WHERE {} {} ?".format(column1, column2, mode), entry))
#         return session.fetchone()[0]

# #DONE
# #  This function returns all of a users data corresponding to the userID in the Users table
# def selectAllUserData(userID):
#     userID = (userID,)
#     with openDB(DB_Location) as session:
#         session.execute(text("SELECT username, forename, surname, email FROM Users WHERE userID = ?", userID))
#         return session.fetchone()

# #DONE
# # Deletes user from Users table and all cards with corresponding userID
# def deleteUser(userID):
#     userID = (userID,)
#     with openDB(DB_Location) as session:
#         session.execute(text("DELETE FROM Cards WHERE userID = ?", userID))
#         session.execute(text("DELETE FROM Users WHERE userID = ?", userID))


# #DONE
# # This function returns all of the cards in the table Cards which belong to a user with the userID passed in
# # as a parameter.
# def selectUserCards(userID):
#     userID = (userID,)

#     with openDB(DB_Location) as session:
#         session.execute(text("SELECT question, answer, cardID FROM Cards WHERE userID = ?", userID))
#         return session.fetchall()

# #DONE
# # This function returns one card with a matching cardID
# def selectThisCard(cardID):
#     cardID = (cardID,)

#     with openDB(DB_Location) as session:
#         session.execute(text("SELECT question, answer, userID FROM Cards WHERE cardID = ?", cardID))
#         return session.fetchone()

# #DONE
# # This function updates the question and answer of a card with the corresponding passed in cardID.
# def updateUserCard(question, answer, cardID):
#     data = (question, answer, cardID)

#     with openDB(DB_Location) as session:
#         session.execute(text("UPDATE Cards SET question = ?, answer = ? WHERE cardID = ?", data))

# #DONE
# # This function creates a card in the database
# def createCard(question, answer, userID):

#     data = (question, answer, userID)

#     with openDB(DB_Location) as session:
#         session.execute(text("INSERT INTO Cards (question, answer, userID) VALUES (?,?,?)", data))

# #DONE
# # This function deletes card with corresponding cardID
# def deleteCard(cardID):

#     cardID = (cardID,)

#     with openDB(DB_Location) as session:

#         session.execute(text("DELETE FROM Cards WHERE cardID = ?", cardID))


# #DONE
# # This function counts how many cards a user has by counting how many cards have a matching userID.
# def countUserCards(userID):
#     userID = (userID,)

#     with openDB(DB_Location) as session:
#         session.execute(text("SELECT COUNT(cardID) FROM Cards WHERE userID = ?", userID))
#         return session.fetchone()[0]



