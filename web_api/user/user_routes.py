from flask import Flask, render_template, Blueprint, session
from web_api import auth, auth_routes
from services import queries, model




user_routes = Blueprint("user_routes", __name__)

@user_routes.route("/")
def home():
    return userPage()



@user_routes.route("/userPage")
def userPage():
    if loggedIn() == True:
        return render_template("userPage.html")

    else:
        return auth.userNotLoggedIn()


@user_routes.route("/editUserDetails", methods=["GET", "POST"])
def editUserDetails():
    if loggedIn() == True:

        if request.method == "POST":

            username = request.form.get("username")
            email = request.form.get("email")
            forename = request.form.get("forename")
            surname = request.form.get("surname")

            # Check username and email are not already present in the DB

            if username != '':

                

                if not queries.check_unique_username(username):
                    flash("Error - Username already registered.", "danger")
                    username = ""

            if email != '':

                

                if not queries.check_unique_email(email):
                    flash("Error - Email already registered.", "danger")
                    email = ""

            
            #loads user information into a user instance based on current id stored in session 
            
            user = model.User(username=username, forename=forname, surname=surname, email=email, id=session["user_id"])
            
            user.commit_changes()
            
            

            return render_template("editUserDetails.html")

        else:
            return render_template("editUserDetails.html")
    else:
        return userNotLoggedIn()



@user_routes.route("/changePassword", methods=["GET", "POST"])
def changePassword():
    if loggedIn() == True:

        if request.method == "POST":

            if request.form.get("mode") == "input":


                #loads user data
                user = Model.User(id = session["user_id"])



                # Checks password in DB matches entered old password.
                if check_password(user.password, request.form.get("oldPassword")):
 
                    newPassword = hash_password(request.form.get("newPassword"))

                    # Checking new password and confirm password match
                    if check_password(newPassword, request.form.get("confirmPassword")):

                        
                        user.password = newPassword
                        user.commit_changes()
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
        return auth.userNotLoggedIn()


# Not yet implemented
@user_routes.route("/deleteUser", methods=["GET", "POST"])
def deleteUser():
    if loggedIn() == True:
        
        user = Model.User(id = session["user_id"])
        user.delete_user()
        session["user_id"] = ""
        flash("Account Deleted.", "success")
        return auth_routes.logout()

    else:
        return userNotLoggedIn()