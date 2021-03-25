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