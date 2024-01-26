'''Import statements'''
from flask import jsonify, request, Blueprint
from lib.twilio_client import send_message, global_var
from lib.helper_functions import ask_questions, is_int


routes = Blueprint('routes', __name__)


@routes.route("/api/callback", methods=["POST"])
def callback_url():
    """callback URL for getting user's reply"""
    query = global_var.get('query')

    # get user's reply
    message = request.form.get("Body")

    # send Initial message to user
    if query == -1 and "hi" in message.lower():
        send_message("Hi there, would you be interested in a short technical quiz?\n  1. Yes\n  2. No\n  reply 1 or 2")
        global_var["query"] += 1
        return jsonify({ "message": "first message sent successfully." }), 200

    # check if entered value is integer or not
    if query >= 0 and not is_int(message):
        return jsonify({ "message": "User entered invalid answer" }), 200

    reply = int(message)
    # check if user replied 1(Yes) or 2(No) or not
    if query == 0 and reply != 1 and reply != 2:
        send_message("Please enter answer from 1 or 2. Try again!")
        return jsonify({ "message": "User entered invalid answer" }), 200

    if query>0 and reply != 1 and reply != 2 and reply != 3 and reply != 4:
        send_message("Please enter answer from 1, 2, 3 or 4. Try again!")
        return jsonify({ "message": "User entered invalid answer" }), 200

    # Reset query if user is not interested
    if query == 0 and reply == 2:
        send_message("Alright, thanks for your reply. Have a nice day!\nType 'hi' to start the chat again")
        global_var["query"] = -1
        return jsonify({ "message": "User is not interested in quiz." }), 200


    # call the function which asks questions to user
    ask_questions(reply)

    return jsonify({"message":"post request made successfully."}), 200
