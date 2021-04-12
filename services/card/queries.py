def return_user_cards(user_id):
        try:
            cards = DB.return_user_cards(user_id)
        except:
            print(sys.exc_info()[0])

        return cards