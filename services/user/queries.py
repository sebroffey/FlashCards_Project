def get_user_by_username(username):   
    return DB.return_userID_with_username(username)

    
def get_user_by_email(email):
    return DB.return_userID_with_email(email)

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