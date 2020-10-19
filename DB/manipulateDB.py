import _sqlite3


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

