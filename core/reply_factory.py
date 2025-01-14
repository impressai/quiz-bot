
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
    Validates and stores the answer for the current question in the Django session.
    '''
    if current_question_id is None or current_question_id < 0 or current_question_id >= len(PYTHON_QUESTION_LIST):
        return False, "Invalid question ID."

    correct_answer = PYTHON_QUESTION_LIST[current_question_id]["answer"]
    session[f"answer_{current_question_id}"] = answer

    # Validate if the answer is correct
    if answer != correct_answer:
        return False, "Incorrect answer. Try again!"

    return True, ""


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    if current_question_id is None or current_question_id < 0 or current_question_id >= len(PYTHON_QUESTION_LIST):
        return "Invalid question ID", -1

    next_index = current_question_id + 1

    if next_index < len(PYTHON_QUESTION_LIST):
        # Return the next question and its ID
        next_question = PYTHON_QUESTION_LIST[next_index]["question_text"]
        return next_question, next_index
    else:
        return None, -1  # No more questions


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    score = 0
    total_questions = len(PYTHON_QUESTION_LIST)

    for question_id in range(total_questions):
        answer_key = f"answer_{question_id}"
        if answer_key in session:
            user_answer = session[answer_key]
            correct_answer = PYTHON_QUESTION_LIST[question_id]["answer"]
            if user_answer == correct_answer:
                score += 1

    # Calculate the percentage score
    percentage = (score / total_questions) * 100
    return f"Your final score is {score}/{total_questions} ({percentage:.2f}%)"
