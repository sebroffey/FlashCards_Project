import sys
from data import DB
from flask import current_app
from extensions import db


class User(db.Model):
    id = db.Column("userID", db.Integer, primary_key=True, autoincrement=True)
    username = db.Column("username", db.String)
    password = db.Column("password", db.String)
    forename = db.Column("forname", db.String)
    surname = db.Column("surname", db.String)
    email = db.Column("email", db.String)

    cards = db.relationship("cards", backref="user", lazy=True)

    def __init__(self, user):
        
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
            

     

    def __repr__(self):
        return "<User %r>" % self.username

    def commit_user(self):
        try:
            self.id = DB.insert_new_user(self)
        except:
            print(sys.exc_info()[0])

    def commit_changes(self):
        try:
            DB.commit_changes(self)
        except:
            print(sys.exc_info()[0])

    def commit_new_password(self):
        try:
            DB.update_user_password(self)
        except:
            print(sys.exc_info()[0])


    def load_user(self):
        try:
            DB_user = DB.load_user(self)
        except:
            print(sys.exc_info()[0])

        new_user = User(DB_user.username, DB_user.password, DB_user.forname, DB_user.surname, DB_user.email, DB_user.id)
        self.__dict__.update(new_user.__dict__)

    

    def count_cards(self):
        try:
            count = DB.count_cards(self)
        except:
            print(sys.exc_info()[0])
        
        return count

    def delete_user(self):
        try:
            DB.delete_user(self)
        except:
            print(sys.exc_info()[0])


 
        
class Card(db.Model):
    id = db.Column("cardID", db.Integer, primary_key=True, autoincrement=True)
    question = db.Column("question", db.String)
    answer = db.Column("answer", db.String)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __init__(card):
    
        if card.question:
            self.question = card.question
        if card.answer:
            self.answer = card.answer
        if card.userID:
            self.userID = card.userID

        if card.id:
            self.id = card.id
            



    def __repr__(self):
        return "<Card %r>" % self.id     

    def commit_card(self):
        try:
            self.id = DB.insert_new_card(self)
            
        except:
            print(sys.exc_info()[0])

    def load_card(self):
        try:
            DB_card = DB.load_card(self)
        except:
            print(sys.exc_info()[0])

        new_card = Card(DB_card.question, DB_card.answer, DB_card.user_id, DB_card.id)
        self.__dict__.update(new_card.__dict__)

    def delete_card(self):
        try:
            DB.delete_card(self)
        except:
            print(sys.exc_info()[0])


    



       