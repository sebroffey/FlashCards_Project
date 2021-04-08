import sys
from data import DB
from flask import current_app


class User(session.Model):

    def __init__(username, password, forename, surname, email, id):
        
        if username:
            self.username = username
        if password:
            self.password = password
        if forename:
            self.forename = forename
        if surname:
            self.surname = surname
        if email:
            self.email = email
        
        if id:
            self.id = id
            load_user()

     

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


 
        
    class Card(session.Model):

        def __init__(question, answer, user_id, id):
        
            if question:
                self.question = question
            if answer:
                self.answer = answer
            if userID:
                self.userID = userID

            if id:
                self.id = id
                load_card()

    
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


    



       