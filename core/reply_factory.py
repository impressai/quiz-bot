
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
    if current_question_id is None or current_question_id < 0:
        return True, ""

    if current_question_id >= len(PYTHON_QUESTION_LIST):
        return False, "Invalid Question ID"

    session[current_question_id] = {
        "user_answer": answer,
        "original_answer": PYTHON_QUESTION_LIST[current_question_id]["answer"],
        "score": 1 if answer == PYTHON_QUESTION_LIST[current_question_id]["answer"] else 0
    }

    return True, ""


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    if current_question_id is None:
        current_question_id = -1

    if current_question_id+1 >= len(PYTHON_QUESTION_LIST):
        return (None, -1)

    return ([PYTHON_QUESTION_LIST[current_question_id+1]['question_text'], PYTHON_QUESTION_LIST[current_question_id+1]['options']], current_question_id+1)


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    result = 0
    for index in range(len(PYTHON_QUESTION_LIST)):
        result += session[str(index)]["score"]
    return f"Your Final Score: {(result/len(PYTHON_QUESTION_LIST))*100}%."
