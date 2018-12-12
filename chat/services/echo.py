def user():
    data = {
        "name": "Echo Service",
        "email": "echo@imessenger.com",
        "imageUrl": ""
    }
    return data


def welcome(user):
    return "Welcome to iMessage. This is an echo service."


def message(user, message):
    return "You sent : %s" % message
