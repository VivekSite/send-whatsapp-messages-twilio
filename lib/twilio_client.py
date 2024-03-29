'''import statements'''
import os
from twilio.rest import Client

# Some Global Variables
global_var = {
    "score": 0,
    "query": -1
}


SENDER = os.environ["TWILIO_SENDER"]
RECEIVER = os.environ["TWILIO_RECEIVER"]


# client instance of twilio
account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)


def send_message(message):
    '''Function to send a message'''
    client.messages.create(
        body = message,
        from_ = SENDER,
        to = RECEIVER,
    )
