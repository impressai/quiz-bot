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
    Validates and stores the answer for the current question to the django session.
    '''
    if current_question_id is None:
        return True, ""

    try:
        question = PYTHON_QUESTION_LIST[current_question_id]
        correct_answer = question["answer"]

        if answer.lower().strip() == correct_answer.lower().strip():
            session["score"] = session.get("score", 0) + 1

        session["answers"] = session.get("answers", {})
        session["answers"][current_question_id] = answer
    except (IndexError, KeyError):
        return False, "Invalid question ID or answer."

    return True, ""


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    if current_question_id is None:
        return PYTHON_QUESTION_LIST[0]["question"], 0

    next_question_id = current_question_id + 1

    if next_question_id < len(PYTHON_QUESTION_LIST):
        return PYTHON_QUESTION_LIST[next_question_id]["question"], next_question_id

    return None, None


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    score = session.get("score", 0)
    total_questions = len(PYTHON_QUESTION_LIST)
    final_response = f"You have completed the quiz! Your score is {score} out of {total_questions}."
    return final_response
