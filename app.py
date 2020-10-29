from flask import Flask, render_template, request, flash, redirect, url_for, session
from DB import DB
import uuid
import hashlib
import random

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

                if countData > 0:
                    username[0] = username[0] + countString

                data = (username[0], passwordHash, forename, surname, email)

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
@app.route("/changePassword", methods=["GET", "POST"])
def changePassword():
    if loggedIn() == True:

        if request.method == "POST":

            if request.form.get("mode") == "input":

                # Checks password in DB matches entered old password.
                if check_password(DB.selectUserDataFromDB(session.get("user_id"), "password", "userID", "="),
                                  request.form.get("oldPassword")):

                    newPassword = hash_password(request.form.get("newPassword"))

                    # Checking new password and confirm password match
                    if check_password(newPassword, request.form.get("confirmPassword")):

                        column = ["password"]
                        entry = [newPassword]
                        DB.updateUserData(entry, column)
                        flash("Password updated", "success")

                        return redirect(url_for("editUserDetails"))

                    else:
                        flash("New passwords do not match", "danger")
                        return render_template("changePassword.html")

                else:
                    flash("Current password does not match entered old password.", "danger")
                    return render_template("changePassword.html")
            else:

                return render_template("changePassword.html")



        else:
            return render_template("changePassword.html")
    else:
        return userNotLoggedIn()


# Not yet implemented
@app.route("/deleteUser", methods=["GET", "POST"])
def deleteUser():
    if loggedIn() == True:

        DB.deleteUser(session.get("user_id"))
        flash("Account Deleted.", "success")
        return logout()

    else:
        return userNotLoggedIn()


@app.route("/editCardsPage", methods=["GET", "POST"])
def editCardsPage():
    print("edit cards page reached")
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
    print("edit this card page reached")
    if loggedIn() == True:

        if request.method == "POST":

            cardID = request.form.get("cardID")
            print(cardID)
            if request.form.get("selection") == "edit":
                card = DB.selectThisCard(cardID)
                return render_template("editThisCard.html", card=card)

            elif request.form.get("selection") == "delete":

                DB.deleteCard(cardID)
                flash("Deleted card.", "success")
                return redirect(url_for('editCardsPage'))



            else:
                return redirect(url_for('editCardsPage'))
        else:
            print("Your getting redirected to edit cards page after being in edit this card :(")
            return redirect(url_for('editCardsPage'))

    return userNotLoggedIn()


@app.route("/createCard", methods=["GET", "POST"])
def createCard():
    if loggedIn() == True:

        if request.method == "POST":

            question = request.form.get("question")
            answer = request.form.get("answer")
            userID = session.get("user_id")
            DB.createCard(question, answer, userID)

            flash("Card created.", "success")
            return redirect(url_for("createCard"))



        else:

            return render_template("createCard.html")



    else:
        return userNotLoggedIn()


@app.route("/practicePage", methods=["GET", "POST"])
def practicePage():
    if loggedIn() == True:

        userID = session.get("user_id")
        amountOfCards = DB.countUserCards(userID)
        cards = DB.selectUserCards(userID)

        if request.method == "POST":

            currentCardID = request.form.get("currentCardID")
            cardNumber = 0
            nextCard = False

            for card in cards:

                if nextCard == True:
                    return render_template("practicePage.html", card=card)
                # If current card is the final card in cards, Go back to first card.
                cardNumber = cardNumber + 1
                print(cardNumber)
                print(amountOfCards)
                # if cardNumber == amountOfCards:
                #     break
                print(card[2])
                print(currentCardID)
                if str(card[2]) == currentCardID:
                    nextCard = True
                print(nextCard)

            print("hrer")
            return render_template("practicePage.html", card=cards[0])


        else:

            # Checks if the user actually has cards to practice with.
            if amountOfCards > 0:
                return render_template("practicePage.html", card=cards[0])
            else:

                flash("You currently have no cards to practice with.", "danger")
                return redirect(url_for("editCardsPage"))
    else:
        return userNotLoggedIn()


@app.route("/testInformation", methods=["GET", "POST"])
def testInformation():
    if loggedIn() == True:

        if request.method == "POST":

            # Render test results

            cards = request.form.get("cards")
            scoreArray = request.form.get("score")
            score = 0

            for result in scoreArray:
                if result == 1:
                    score = score + 1


            return render_template("testResults.html", cards=cards, scoreArray=scoreArray, score=score)



        else:
            return render_template("testInformation.html", amountOfCards=DB.countUserCards(session.get("user_id")))

    else:
        return userNotLoggedIn()


@app.route("/testInProgress", methods=["GET", "POST"])
def testInProgress():
    if loggedIn() == True:

        if request.method == "POST":

            index = int(request.form.get("index"))
            cards = request.form.get("cards")
            score = request.form.get("score")
            enteredAnswer = request.form.get("enteredAnswer")

            # annoyingly form passes cards array as string hence this conversion of the string to an array:
            cards = cards.replace("[","")
            cards = cards.replace("(","")

            cards = cards[0, len(cards)-2]

            cardsConversionArray = cards.split("),")

            amountOfCards = DB.countUserCards(session.get("user_id"))
            data = 0
            cardsArray = [[data for i in range(10)] for j in range(amountOfCards-1)]

            for index in range(0, len(cardsConversionArray) - 1):

                cardsConversionArray[index] = cardsConversionArray[index].trim()
                singleCard = cardsConversionArray[index].split(", ")

                for index2 in range(0, len(singleCard)-1):
                    cardsArray[index][index2]


            if enteredAnswer == cards[index][1]:
                score = score.append(1)
            else:
                score = score.append(enteredAnswer)

            index = index + 1

            return render_template("testInProgress.html", index=index, cards=cards, score=score)











        else:

            # Loads and shuffles cards
            userID = session.get("user_id")
            cards = DB.selectUserCards(userID)
            random.shuffle(cards)

            # Creates score array
            score = []
            return render_template("testInProgress.html", index=0, cards=cards, score=score)




    else:
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
