from flask import Flask, render_template, Blueprint
from . import auth
auth_routes = Blueprint("auth_routes", __name__)

@auth_routes.route("/registerUser", methods=["GET", "POST"])
def registerUser():
    if request.method == "POST":

        passwordHash = auth.hash_password(request.form.get("password"))

        # Check if two passwords are equal:
        if auth.check_password(passwordHash, request.form.get("confirm_password")) == True:

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


@auth_routes.route("/loginUser", methods=["GET", "POST"])
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

        if auth.check_password(storedHash, request.form.get("password")) == True:

            # Passwords match
            return validLogin(userID)

        else:

            # passwords dont match
            flash("Incorrect password", "danger")
            return render_template('login.html')

    return render_template('login.html')


@auth_routes.route("/logout")
def logout():
    if session.get("user_id") is not None:

        session.pop("user_id")
        flash("Logged out " + session.get("username"))
        session.pop("username")
        return render_template("home.html")

    else:
        return render_template('home.html')



