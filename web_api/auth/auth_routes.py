from flask import Flask, render_template, Blueprint, session
from . import auth
from services import model, card
from services import user as s_user


auth_routes = Blueprint("auth_routes", __name__)

@auth_routes.route("/registerUser", methods=["GET", "POST"])
def registerUser():
    if request.method == "POST":

        passwordHash = auth.hash_password(request.form.get("password"))

        # Check if two passwords are equal:
        if auth.check_password(passwordHash, request.form.get("confirm_password")) == True:

            #Create user model for database querying
            user = model.User(email = request.form.get("email"))

            
            # Check email is not already being used
            # search db for email
            

            
            


            if not queries.check_unique_email(user.email):
                flash("Email entered is already registered to a user.", "danger")
                return render_template("register.html")

            else:

                # Register User
                user.forename = request.form.get("forename").capitalize()
                user.surname = request.form.get("surname").capitalize()

                user.username = forename + surname
                
                countData = 0
                
                

                while not queries.check_unique_username(user.username):

                    countData = countData + 1

                    if countData > 1:
                        previousCountStringLength = len(countString)
                        countString = str(countData)
                        user.username = username[0:len(user.username)-previousCountStringLength] + countString
                    else:
                        user.username = username + str(countData)

                user.password = passwordHash

                # Insert New User into DB
                user.commit_user()

                flash("User Created, note down your generated username: " + user.username, "success")
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

            

            

            if queries.check_unique_email(user.email):
                # No username or email found
                flash("Email not registered.", "danger")
                return render_template('login.html')

            else:
                user = s_user.get_user_by_email(usernameOrEmail)

        else:

            # Log in by username
            user.username = usernameOrEmail
            if queries.check_unique_username(user.username):
                # No username or email found
                flash("Incorrect username.", "danger")
                return render_template('login.html')

            else:
                user = queries.load_user(False, user.username)

        if auth.check_password(user.password, request.form.get("password")) == True:

            # Passwords match
            return auth.validLogin(user)

        else:

            # passwords dont match
            del user 
            flash("Incorrect password", "danger")
            return render_template('login.html')

    return render_template('login.html')


@auth_routes.route("/logout")
def logout():
    if session.get("user_id") is not None:

        session.pop("user_id")
        flash("Logged out")
        return render_template("home.html")

    else:
        return render_template('home.html')



