from itertools import count

from flask import Flask, render_template, request, flash, redirect, url_for, session
import _sqlite3
from DB import manipulateDB


# session stores values in a dict
def loggedIn():
    if session.get("user_id"):
        return True
    else:
        return False


# using code to hash passwords with salt https://www.pythoncentral.io/hashing-strings-with-python/
import uuid
import hashlib


def hash_password(password):
    # uuid is used to generate a random number
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt


# Will return true or false
def check_password(hashed_password, entered_password):
    password, salt = hashed_password.split(':')
    if password == hashlib.sha256(salt.encode() + entered_password.encode()).hexdigest():
        return True
    else:
        return False


app = Flask(__name__)
manipulateDB.innitializeUser_DB()

DB_Location = "DB/User_Data.db"
app.config["SECRET_KEY"] = "secretkey"


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/registerUser", methods=["GET", "POST"])
def registerUser():
    if request.method == "POST":

        passwordHash = hash_password(request.form.get("password"))

        # Check if two passwords are equal:
        if check_password(passwordHash, request.form.get("confirm_password")) == True:

            # Check email is not already being used
            # Question, why does it only work when email is a tuple as well as email tuple? lol
            email = (request.form.get("email"),)

            emailTuple = (email[0],)
            # search db for email
            with manipulateDB.openDB(DB_Location) as db:
                db.execute("SELECT COUNT(username) FROM Users WHERE email = ?", emailTuple)
                emailExists = db.fetchone()[0]

            if emailExists != 0:
                flash("Email entered is already registered to a user.", "danger")
                return render_template("register.html")

            else:

                # Register User
                forename = request.form.get("forename").capitalize()
                surname = request.form.get("surname").capitalize()

                username = [forename + surname, ]
                seachUsernameInput = (username[0] + '%',)

                with manipulateDB.openDB(DB_Location) as db:
                    db.execute("SELECT COUNT(username) FROM Users WHERE username LIKE ?", seachUsernameInput)
                    data = db.fetchone()[0]
                    db.execute("SELECT COUNT(userID) FROM Users")
                    userID = db.fetchone()[0]

                usernameOccurence = str(data)

                if data > 0:
                    username[0] = username[0] + usernameOccurence

                userID = userID + 1

                data = (username[0], passwordHash, forename, surname, email[0], userID)

                with manipulateDB.openDB(DB_Location) as db:
                    db.execute(
                        "INSERT INTO Users (username, password, forename, surname, email, userID) VALUES (?,?,?,?,?,?)",
                        data)

                flash("User Created, note down your generated username: " + username[0], "success")
                return redirect(url_for("loginUser"))

        else:
            flash("Passwords do not match", "danger")

    return render_template("register.html")


@app.route("/loginUser", methods=["GET", "POST"])
def loginUser():
    if request.method == "POST":

        # Different methods of logging in, just for practice either by email or username.

        usernameOrEmail = (str(request.form.get("username")),)

        if usernameOrEmail[0].find("@") != -1:

            # Log in by email
            with manipulateDB.openDB(DB_Location) as db:
                db.execute("SELECT COUNT(username) FROM Users WHERE email = ?", usernameOrEmail)
                data = db.fetchone()[0]

            if data == 0:
                # No username or email found
                flash("Email not registered.", "danger")
                return render_template('login.html')

            else:
                with manipulateDB.openDB(DB_Location) as db:
                    db.execute("SELECT password FROM Users WHERE email = ?", usernameOrEmail)
                    storedHash = db.fetchone()[0]
                    db.execute("SELECT userID FROM Users WHERE email = ?", usernameOrEmail)
                    userID = db.fetchone()[0]
                    db.execute("SELECT username FROM Users WHERE email = ?", usernameOrEmail)
                    username = db.fetchone()[0]





        else:

            with manipulateDB.openDB(DB_Location) as db:
                db.execute("SELECT COUNT(username) FROM Users WHERE username = ?", usernameOrEmail)
                data = db.fetchone()[0]

            if data == 0:
                # No username or email found
                flash("Incorrect username.", "danger")
                return render_template('login.html')

            else:
                with manipulateDB.openDB(DB_Location) as db:
                    db.execute("SELECT password FROM Users WHERE username = ?", usernameOrEmail)
                    storedHash = db.fetchone()[0]
                    db.execute("SELECT userID FROM Users WHERE username = ?", usernameOrEmail)
                    userID = db.fetchone()[0]
                username = usernameOrEmail[0]

        if check_password(storedHash, request.form.get("password")) == True:

            # Passwords match
            flash("Correct Password", "success")
            session["user_id"] = userID
            session["username"] = username
            return render_template('userPage.html')

        else:

            # passwords dont match
            flash("Incorrect password", "danger")
            return render_template('login.html')

    return render_template('login.html')


@app.route("/logout")
def logout():
    session.pop("user_id")

    flash("Logged out " + session.get("username"))
    session.pop("username")
    return render_template("home.html")
