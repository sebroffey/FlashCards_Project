import sys
from data import DB


def load_user(search_by, value):

    # True for via email, Flase for via username
    if search_by:
        user = DB.return_userID_with_email(value)
    else:
        user = DB.return_userID_with_username(value)

    return user


def check_unique_username(username):
    try:
        status = DB.check_unique_username(username)
    except:
        print(sys.exc_info()[0])
        
    return status


def check_unique_email(email):
    try:
        status = DB.check_unique_email(email)
    except:
        print(sys.exc_info()[0])

    return status

def return_user_cards(user_id):
        try:
            cards = DB.return_user_cards(user_id)
        except:
            print(sys.exc_info()[0])

        return cards