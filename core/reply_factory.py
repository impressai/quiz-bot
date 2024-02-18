
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
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
    que = PYTHON_QUESTION_LIST[current_question_id]
    answer = answer.strip()
    if not 'user_resp' in session:
        session['user_resp'] = {}
    session['user_resp'][current_question_id] = que['answer'] == answer, answer
    session.save()
    return True, ""


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    if current_question_id == (len(PYTHON_QUESTION_LIST) - 1):
        return None, None
    que = PYTHON_QUESTION_LIST[current_question_id + 1]

    return que['question_text'], current_question_id + 1


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    score = 0
    user_resp = session['user_resp']
    for qid in user_resp:
        if user_resp[qid][0] == True:
            score += 1
    return f"User Score: {score} correct out of {len(PYTHON_QUESTION_LIST)}"
