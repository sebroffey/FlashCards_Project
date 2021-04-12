class Config():

    SECRET_KEY = "secretkey"
    SESSION_PERMANENT = False

    SQLALCHEMY_DATABASE_URI = 'sqlite:////DB/DB.session'
    SQLALCHEMY_ECHO = True #For Debugging