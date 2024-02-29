
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if current_question_id == 0:
        pass
    elif not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to django session.
    '''
    if not session.get('answers'):
        session['answers'] = {}

    # Store the answer for the current question in the session
    if current_question_id or current_question_id == 0:
        session['answers'][current_question_id] = answer
        session.save()
        
    return True, ""


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    question_list_length = len(PYTHON_QUESTION_LIST)
    if (current_question_id == question_list_length - 1):
        return False, -1
    elif (current_question_id or current_question_id == 0):
        return PYTHON_QUESTION_LIST[current_question_id+1], current_question_id + 1
    else:
        return PYTHON_QUESTION_LIST[0], 0




def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    question_len = len(PYTHON_QUESTION_LIST)
    answers = session.get('answers')
    point = 0
    for i in range(0, question_len):
        answer = answers[i]
        right_answer = PYTHON_QUESTION_LIST[i]['answer']

        if (answer == right_answer):
            point += 1

    return f"Hey Buddy, Your Final Score is : {point}"
