from flask import Flask, render_template, Blueprint, session
from services import model
from web_api import auth
import random


card_routes = Blueprint("card_routes", __name__)




@card_routes.route("/editCardsPage", methods=["GET", "POST"])
def editCardsPage():
    
    if auth.loggedIn():

        userID = session.get("user_id")

        if request.method == "POST":

            
            question = request.form.get("question")
            answer = request.form.get("answer")
            cardID = request.form.get("cardID")
            #create card instance
            card = model.Card(id=cardID)
            card.__init__(question=question, answer=answer)
            card.commit_changes()
            flash("Card Updated Successfully", "success")

        
        cards = query.return_user_cards(userID)
        amountOfCards = len(cards)

        return render_template("editCardsPage.html", cards=cards, amountOfCards=amountOfCards)



    else:

        return userNotLoggedIn()


@card_routes.route("/editThisCard", methods=["GET", "POST"])
def editThisCard():
    
    if auth.loggedIn():

        if request.method == "POST":

            cardID = request.form.get("cardID")
            #create card model
            card = model.Card(id=cardID)

            if request.form.get("selection") == "edit":
                
                return render_template("editThisCard.html", card=card)

            elif request.form.get("selection") == "delete":

                card.delete_card()
                flash("Deleted card.", "success")
                return redirect(url_for('editCardsPage'))



            else:
                return redirect(url_for('editCardsPage'))
        else:
            
            return redirect(url_for('editCardsPage'))

    return userNotLoggedIn()


@card_routes.route("/createCard", methods=["GET", "POST"])
def createCard():
    if auth.loggedIn():

        if request.method == "POST":
            
            
            question = request.form.get("question")
            answer = request.form.get("answer")
            userID = session.get("user_id")
            
            #create model card
            card = model.Card(question=question, answer=answer, user_id=userID)
            card.commit_card()

            flash("Card created.", "success")
            return redirect(url_for("createCard"))



        else:

            return render_template("createCard.html")



    else:
        return userNotLoggedIn()


@card_routes.route("/practicePage", methods=["GET", "POST"])
def practicePage():
    if auth.loggedIn():

        userID = session.get("user_id")
        cards = queries.return_user_cards(userID)
        

        if request.method == "POST":

            currentCardID = request.form.get("currentCardID")
            cardNumber = 0
            nextCard = False

            for card in cards:

                if nextCard == True:
                    return render_template("practicePage.html", card=card)
                # If current card is the final card in cards, Go back to first card.
                cardNumber = cardNumber + 1
              
                # if cardNumber == amountOfCards:
                #     break
                
                if str(card.id) == currentCardID:
                    nextCard = True
                

            
            return render_template("practicePage.html", card=cards[0])


        else:

            # Checks if the user actually has cards to practice with.
            if cards:
                return render_template("practicePage.html", card=cards[0])
            else:

                flash("You currently have no cards to practice with.", "danger")
                return redirect(url_for("editCardsPage"))
    else:
        return userNotLoggedIn()


@card_routes.route("/testInformation", methods=["GET", "POST"])
def testInformation():
    if auth.loggedIn():

        if request.method == "POST":

            # Render test results
            index = int(request.form.get("index"))



            return render_template("testResults.html", index=index)



        else:
            return render_template("testInformation.html", amountOfCards=len(queries.return_user_cards(session.get("user_id")))

    else:
        return auth.userNotLoggedIn()


@card_routes.route("/testInProgress", methods=["GET", "POST"])
def testInProgress():
    if auth.loggedIn():

        # Should change so this isnt repeated
        cards = queries.return_user_cards(session.get("user_id"))
        amountOfCards = len(cards)

        if request.method == "POST":

            index = int(request.form.get("index"))
            enteredAnswer = request.form.get("enteredAnswer")
            index = index + 1




            return render_template("testInProgress.html", index=index, enteredAnswer=enteredAnswer, amountOfCards=amountOfCards)











        else:

            # Loads and shuffles cards
            userID = session.get("user_id")
            
            random.shuffle(cards)

            #Need to rid of tuples for js

            jsonArrayCards = []

            for card in cards:

                jsonCard = {"question": card.question, "answer": card.answer, "cardID": card.id}

                jsonArrayCards.append(jsonCard)

            # Creates score array

            return render_template("testInProgress.html", index=0, cards=jsonArrayCards, amountOfCards=amountOfCards)




    else:
        return auth.userNotLoggedIn()

