import sys
from data import DB

class User(session.Model):

    def __init__(username, password, forename, surname, email):

        self.username = username
        self.password = password
        self.forename = forename
        self.surname = surname
        self.email = email

        

    def __repr__(self):
        return "<User %r>" % self.username

    def commit_user():
        try:
            DB.insertNewUser(self)
        except:
            print(sys.exc_info()[0])

    def commit_change(attribute):
        try:
            DB.updateUserData(attribute, self)
        except:
            print(sys.exc_info()[0])

    class Card(session.Model):
        question = session.Column("question", session.String)
        answer = session.Column("answer", session.String)
        cardID = session.Column("cardID", session.Integer, primary_key=True, autoincrement=True)
        userID = session.Column(session.Integer, session.ForeignKey("users.userID"), nullable=False)
        users = session.relationship("Users", backref=session.backref("cards", lazy=True))