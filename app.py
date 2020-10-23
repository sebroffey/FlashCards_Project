from flask import Flask, render_template, request, flash, redirect, url_for, session
from DB import DB
import uuid
import hashlib

app = Flask(__name__)
DB.innitializeUser_DB()

app.config["SECRET_KEY"] = "secretkey"
app.config["SESSION_PERMANENT"] = False


# using code to hash passwords with salt https://www.pythoncentral.io/hashing-strings-with-python/
def hash_password(password):
    # uuid is used to generate a random number
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt


# Checks if two passwords are the same, Will return true or false
def check_password(hashed_password, entered_password):
    password, salt = hashed_password.split(':')
    if password == hashlib.sha256(salt.encode() + entered_password.encode()).hexdigest():
        return True
    else:
        return False


# Prevents repeat code across program for checking if a user is logged in, returns a boolean.
def loggedIn():
    if session.get("user_id"):
        return True
    else:
        return False


# Prevents repeating code for when a user is redirected after not being logged in.
def userNotLoggedIn():
    flash("Please log in.", "danger")
    return render_template("login.html")


# Function called after user logs in or user details are changed
# session stores values to be called whenever they need rendering on a html page.
def refreshSession(userID):
    user = DB.selectAllUserData(userID)

    session["username"] = user[0]
    session["forename"] = user[1]
    session["surname"] = user[2]
    session["email"] = user[3]
    session["user_id"] = userID


# Function for when a user logs in which does all of the required steps to log a user in
# including redirecting them to their user page.
def validLogin(userID):
    refreshSession(userID)
    flash("Correct Password, Welcome " + session.get("forename"), "success")
    return render_template('userPage.html')


#
# APP ROUTES
#


@app.route("/")
def home():
    return logout()


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


# Not yet implemented
@app.route("/changePassword")
def changePassword():
    if loggedIn() == True:

        if request.method == "POST":

            print()
            # Not Finished This Link, will show a method error
            return render_template("editUserDetails.html")

        else:
            return render_template("editUserDetails.html")
    else:
        return userNotLoggedIn()


# Not yet implemented
@app.route("/deleteUser")
def deleteUser():
    if loggedIn() == True:

        if request.method == "POST":

            print()
            # Not Finished This Link, will show a method error
            return render_template("editUserDetails.html")

        else:
            return render_template("editUserDetails.html")
    else:
        return userNotLoggedIn()


@app.route("/editCardsPage", methods=["GET", "POST"])
def editCardsPage():
    if loggedIn() == True:

        if request.method == "POST":
            question = request.form.get("question")
            answer = request.form.get("answer")
            cardID = request.form.get("cardID")
            DB.updateUserCard(question, answer, cardID)

            flash("Card Updated Successfully", "success")

        userID = session.get("user_id")
        cards = DB.selectUserCards(userID)
        amountOfCards = DB.countUserCards(userID)

        return render_template("editCardsPage.html", cards=cards, amountOfCards=amountOfCards)



    else:

        return userNotLoggedIn()


@app.route("/editThisCard", methods=["GET", "POST"])
def editThisCard():
    if loggedIn() == True:

        if request.method == "POST":

            cardID = request.form.get("cardID")

            if request.form.get("selection") == "edit":
                card = DB.selectThisCard(cardID)
                return render_template("editThisCard.html", card=card)

            else:
                return redirect(url_for('editCardsPage'))
        else:
            return redirect(url_for('editCardsPage'))

    return userNotLoggedIn()


@app.route("/logout")
def logout():
    if session.get("user_id") is not None:

        session.pop("user_id")
        flash("Logged out " + session.get("username"))
        session.pop("username")
        return render_template("home.html")

    else:
        return render_template('home.html')
