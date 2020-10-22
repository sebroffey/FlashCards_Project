from itertools import count

from flask import Flask, render_template, request, flash, redirect, url_for, session
import _sqlite3
from DB import DB

app = Flask(__name__)
DB.innitializeUser_DB()

app.config["SECRET_KEY"] = "secretkey"
app.config["SESSION_PERMANENT"] = False

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


# session stores values in a dict
def loggedIn():
    if session.get("user_id"):
        return True
    else:
        return False


def userNotLoggedIn():
    flash("Please log in.", "danger")
    return render_template("login.html")


def refreshSession(userID):
    user = DB.selectAllUserData(userID)

    session["username"] = user[0]
    session["forename"] = user[1]
    session["surname"] = user[2]
    session["email"] = user[3]
    session["user_id"] = userID


def validLogin(userID):
    refreshSession(userID)
    flash("Correct Password, Welcome " + session.get("forename"), "success")
    return render_template('userPage.html')


# WEDNESDAY


# Forget password change and delete user for now
# Focus on implementing storing cards next
# Maybe blueprints
# Document using sphinx at some point


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
            # search db for email
            email = request.form.get("email")

            if DB.countEntryInUsers(email, "email", "email", "=") != 0:
                flash("Email entered is already registered to a user.", "danger")
                return render_template("register.html")

            else:

                # Register User
                forename = request.form.get("forename").capitalize()
                surname = request.form.get("surname").capitalize()

                username = [forename + surname, ]
                seachUsernameInput = (username[0] + '%',)

                countData = DB.countEntryInUsers(seachUsernameInput[0], "username", "username", "LIKE")
                countString = str(countData)

                userID = DB.countEntryInUsers(None, "userID", "userID", "ALL")

                if countData > 0:
                    username[0] = username[0] + countString

                userID = userID + 1
                data = (username[0], passwordHash, forename, surname, email, userID)

                # Insert New User into DB
                DB.insertNewUser(data)

                flash("User Created, note down your generated username: " + username[0], "success")
                return redirect(url_for("loginUser"))

        else:
            flash("Passwords do not match", "danger")

    return render_template("register.html")


@app.route("/loginUser", methods=["GET", "POST"])
def loginUser():
    if request.method == "POST":

        # Different methods of logging in, just for practice either by email or username.
        usernameOrEmail = request.form.get("username")

        if usernameOrEmail.find("@") != -1:

            # Log in by email
            occurrence = DB.countEntryInUsers(usernameOrEmail, "username", "email", "=")

            if occurrence == 0:
                # No username or email found
                flash("Email not registered.", "danger")
                return render_template('login.html')

            else:
                storedHash = DB.selectUserDataFromDB(usernameOrEmail, "password", "email", "=")
                userID = DB.selectUserDataFromDB(usernameOrEmail, "userID", "email", "=")

        else:

            # Log in by username
            occurrence = DB.countEntryInUsers(usernameOrEmail, "username", "username", "=")

            if occurrence == 0:
                # No username or email found
                flash("Incorrect username.", "danger")
                return render_template('login.html')

            else:
                storedHash = DB.selectUserDataFromDB(usernameOrEmail, "password", "username", "=")
                userID = DB.selectUserDataFromDB(usernameOrEmail, "userID", "username", "=")

        if check_password(storedHash, request.form.get("password")) == True:

            # Passwords match
            return validLogin(userID)

        else:

            # passwords dont match
            flash("Incorrect password", "danger")
            return render_template('login.html')

    return render_template('login.html')


@app.route("/userPage")
def userPage():
    if loggedIn() == True:
        return render_template("userPage.html")

    else:
        return userNotLoggedIn()


@app.route("/editUserDetails", methods=["GET", "POST"])
def editUserDetails():
    if loggedIn() == True:

        if request.method == "POST":

            username = request.form.get("username")
            email = request.form.get("email")
            forename = request.form.get("forename")
            surname = request.form.get("surname")

            # Check username and email are not already present in the DB

            if username != '':

                occurrence = DB.countEntryInUsers(username, "username", "username", "=")

                if occurrence > 0:
                    flash("Error - Username already registered.", "danger")
                    username = ""

            if email != '':

                occurrence = DB.countEntryInUsers(email, "email", "email", "=")

                if occurrence > 0:
                    flash("Error - Email already registered.", "danger")
                    email = ""

            entries = []
            columns = []
            # Iterate across array to save retyping code
            infoArray = [["username", username], ["email", email], ["forename", forename], ["surname", surname]]

            for index in range(0, len(infoArray)):

                if infoArray[index][1] != '':
                    columns.append(infoArray[index][0])
                    entries.append(infoArray[index][1])

            DB.updateUserData(entries, columns)
            refreshSession(session.get("user_id"))

            return render_template("editUserDetails.html")

        else:
            return render_template("editUserDetails.html")
    else:
        return userNotLoggedIn()


@app.route("/changePassword")
def changePassword():
    if loggedIn() == True:

        if request.method == "POST":

            print()
            # Not Finished This Link, will show a method error

        else:
            return render_template("editUserDetails.html")
    else:
        return userNotLoggedIn()


@app.route("/deleteUser")
def deleteUser():
    if loggedIn() == True:

        if request.method == "POST":

            print()
            # Not Finished This Link, will show a method error

        else:
            return render_template("editUserDetails.html")
    else:
        return userNotLoggedIn()


@app.route("/editCardsPage/<int:cardID>", methods=["GET", "POST"])
def editCardsPage(cardID):
    if loggedIn() == True:

        print("Here2")
        userID = session.get("user_id")
        cards = DB.selectUserCards(userID)
        amountOfCards = DB.countUserCards(userID)

        if request.method == "POST":

            print("here3")
            question = request.form.get("question")
            answer = request.form.get("answer")

            DB.updateUserCard(question, answer, cardID)

            flash("Card Updated Successfully", "success")
            return render_template("editCardsPage.html", cards=cards, amountOfCards=amountOfCards)


        else:
            return render_template("editCardsPage.html", cards=cards, amountOfCards=amountOfCards)



    else:

        return userNotLoggedIn()


@app.route("/editThisCard/<int:cardID>", methods=["GET", "POST"])
def editThisCard(cardID):
    if loggedIn() == True:

        #
        card = DB.selectThisCard(cardID)
        print(card[2])
        print(session.get("user_id"))
        print()
        # Checking card belongs to user who is logged in
        if card[2] == session.get("user_id"):

            return render_template("editThisCard.html", card=card)
            # Card belongs to user
        else:
            pass
            #flash("Card does not exist", "danger")
            #print("Here")
            #return redirect(url_for("editCardsPage", cardID=1))


    return userNotLoggedIn()


@app.route("/logout")
def logout():
    if session.get("user_id") is not None:

        session.pop("user_id")
        flash("Logged out " + session.get("username"))
        session.pop("username")
        return render_template("home.html")

    else:
        return userNotLoggedIn()
