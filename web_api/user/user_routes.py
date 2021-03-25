from flask import Flask, render_template, Blueprint

user_routes = Blueprint("user_routes", __name__)

@user_routes.route("/")
def home():
    return userPage()



@user_routes.route("/userPage")
def userPage():
    if loggedIn() == True:
        return render_template("userPage.html")

    else:
        return userNotLoggedIn()


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
@user_routes.route("/changePassword", methods=["GET", "POST"])
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
@user_routes.route("/deleteUser", methods=["GET", "POST"])
def deleteUser():
    if loggedIn() == True:

        DB.deleteUser(session.get("user_id"))
        flash("Account Deleted.", "success")
        return logout()

    else:
        return userNotLoggedIn()