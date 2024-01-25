"""import statements"""
import os
from flask import Flask, request, jsonify
from twilio.rest import Client
from question import questions as q


app = Flask(__name__)

"""client instance of twilio"""
account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)

# Information of sender and receiver
SENDER = "whatsapp:+14155238886"
RECEIVER = "whatsapp:+919106422767"


# Some Global Variables
score = 0
interested = False
curr_query = 0


client.messages.create(
    body=f"{q[0].get("question")}\n  1. {q[0].get("1")}\n  2. {q[0].get("2")}\n reply 1 or 2",
    from_= SENDER,
    to = RECEIVER,
)

def check_ans(i, reply):
    '''Function to check whether the answer is correct'''
    global score
    global curr_query

    if reply == q[i].get("answer") :
        client.messages.create(
            body="Right answer.",
            from_= SENDER,
            to = RECEIVER,
        )
        score += 1
    else:
        client.messages.create(
            body="Wrong answer, better luck next time!",
            from_= SENDER,
            to = RECEIVER,
        )
    curr_query += 1



def format_question(i):
    '''Function to format a question'''
    return f"{q[i].get("question")}\n  1. {q[i].get("1")}\n  2. {q[i].get("2")}\n  3. {q[i].get("3")}\n  4. {q[i].get("4")}"



def ask_questions(reply):
    '''Finction which asks questions'''
    global curr_query
    global score

    if curr_query == 0:
        client.messages.create(
            body="instruction - You have to answer an MCQ question that has 4 options but only one correct out of them. Send the correct option number in the reply to the question for eg - 2\nType 'restart' to restart the test",
            from_= SENDER,
            to = RECEIVER,
        )
        client.messages.create( body = format_question(1), from_= SENDER, to = RECEIVER )
        curr_query += 1
    elif curr_query == 1:
        check_ans(1, reply)
        client.messages.create( body=format_question(2), from_= SENDER, to = RECEIVER )
    elif curr_query == 2:
        check_ans(2, reply)
        client.messages.create( body=format_question(3), from_= SENDER, to = RECEIVER )
    elif curr_query == 3:
        check_ans(3, reply)
        client.messages.create( body=format_question(4), from_= SENDER, to = RECEIVER )
    elif curr_query == 4:
        check_ans(4, reply)
        client.messages.create( body=format_question(5), from_= SENDER, to = RECEIVER )
    elif curr_query == 5:
        check_ans(5, reply)
        client.messages.create( body=f"Your score is: {score}/5", from_= SENDER, to = RECEIVER )
        curr_query = 1
        score = 0



@app.route("/api/callback", methods=["POST"])
def callback_url():
    """callback URL for getting user's reply"""
    global interested
    global curr_query
    global score

    message = request.form.get("Body")
    # check if user's reply is valid
    try:
        reply = int(message)
    except ValueError:
        client.messages.create(
            body="Enter only integers in reply, Try again",
            from_ = SENDER, to = RECEIVER
        )
        return jsonify({"message":"The string does not represent a valid integer!"}), 400
    
    # check if user is interested or not
    if curr_query == 0 and int(message) == 1:
        interested = True

    # check if reply is 1 2 3 or 4
    if reply > 4 or reply < 1 :
        client.messages.create(
            body="Choose options from 1, 2, 3 or 4, Try again",
            from_ = SENDER, to = RECEIVER
        )
        return jsonify({"message":"Not a valid answer!"}), 400

    if message.lower() == "restart":
        curr_query = 1
        score = 0

    if interested:
        ask_questions(reply)
    else:
        client.messages.create(
            body="Alright, thanks for your reply. Have a nice day!",
            from_= SENDER,
            to = RECEIVER,
        )
    return jsonify({"message":"post request made successfully."}), 200



if __name__ == "__main__":
    app.run(debug=True, port=8080)
