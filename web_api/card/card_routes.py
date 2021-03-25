from flask import Flask, render_template, Blueprint

card_routes = Blueprint("card_routes", __name__)




@card_routes.route("/editCardsPage", methods=["GET", "POST"])
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


@card_routes.route("/editThisCard", methods=["GET", "POST"])
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


@card_routes.route("/createCard", methods=["GET", "POST"])
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


@card_routes.route("/practicePage", methods=["GET", "POST"])
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


@card_routes.route("/testInformation", methods=["GET", "POST"])
def testInformation():
    if loggedIn() == True:

        if request.method == "POST":

            # Render test results
            index = int(request.form.get("index"))



            return render_template("testResults.html", index=index)



        else:
            return render_template("testInformation.html", amountOfCards=DB.countUserCards(session.get("user_id")))

    else:
        return userNotLoggedIn()


@card_routes.route("/testInProgress", methods=["GET", "POST"])
def testInProgress():
    if loggedIn() == True:

        # Should change so this isnt repeated
        amountOfCards = DB.countUserCards(session.get("user_id"))

        if request.method == "POST":

            index = int(request.form.get("index"))
            enteredAnswer = request.form.get("enteredAnswer")
            index = index + 1




            return render_template("testInProgress.html", index=index, enteredAnswer=enteredAnswer, amountOfCards=amountOfCards)











        else:

            # Loads and shuffles cards
            userID = session.get("user_id")
            cards = DB.selectUserCards(userID)
            random.shuffle(cards)

            #Need to rid of tuples for js

            jsonArrayCards = []

            for card in cards:

                jsonCard = {"question": card[0], "answer": card[1], "cardID": card[2]}

                jsonArrayCards.append(jsonCard)

            # Creates score array

            return render_template("testInProgress.html", index=0, cards=jsonArrayCards, amountOfCards=amountOfCards)




    else:
        return userNotLoggedIn()

