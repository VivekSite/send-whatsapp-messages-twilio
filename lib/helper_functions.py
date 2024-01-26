'''Import some useful variables from app'''
from lib.twilio_client import send_message, global_var
from question import questions as q


def is_int(reply):
    '''Validate if answer of question is valid'''
    try:
        int(reply)
        return True
    except ValueError:
        send_message("Please enter integers only in answer.\nTry again")
        return False


def check_ans(i, reply):
    '''Function to check whether the answer is correct'''

    if reply == q[i].get("answer") :
        send_message("Right answer.")
        global_var["score"] += 1
    else:
        send_message("Wrong answer, better luck next time!")
    global_var["query"] += 1


def format_question(i):
    '''Function to format a question'''
    return f"{q[i].get("question")}\n  1. {q[i].get("1")}\n  2. {q[i].get("2")}\n  3. {q[i].get("3")}\n  4. {q[i].get("4")}"


def ask_questions(reply):
    '''Finction which asks questions'''
    query = global_var["query"]

    for i in range(len(q)):
        if query == 0 and i == 0:
            send_message("instruction - You have to answer an MCQ question that has 4 options but only one correct out of them. Send the correct option number in the reply to the question \nfor eg - 2")
            send_message(format_question(query))
            global_var["query"] += 1
            return
        if query == len(q) and i == len(q)-1:
            check_ans(query-1, reply)
            send_message(f"Your score is: {global_var["score"]}/{len(q)}")
            global_var["query"] = 0
            global_var["score"] = 0
            return
        if query == i:
            check_ans(query-1, reply)
            send_message(format_question(query))
            return
