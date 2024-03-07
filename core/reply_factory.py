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
    if current_question_id is not None:
        
        session[current_question_id] = answer
        session.save()
        return True, ""
    else:
        return False, "No current question ID"


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    if current_question_id is None:
        return PYTHON_QUESTION_LIST[0], 0
    elif current_question_id < len(PYTHON_QUESTION_LIST) - 1:
        return PYTHON_QUESTION_LIST[current_question_id + 1], current_question_id + 1
    else:
        return None, None


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    score = calculate_score(session)
    return f"Your final score is: {score}"


def calculate_score(session):
    '''
    Calculates the score based on the answers stored in the session.
    This is just a dummy implementation. You should replace it with your actual scoring logic.
    '''
    score = 0
    for question_id, question in enumerate(PYTHON_QUESTION_LIST):
        if session.get(question_id) == question['correct_answer']:
            score += 1
    return score
