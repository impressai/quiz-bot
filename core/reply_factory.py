
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
    """
    Validates and stores the answer for the current question in the Django session.
    """
    from .constants import PYTHON_QUESTION_LIST  # Import the question list if not already imported
    
    # Retrieve the current question from the question list based on question ID
    current_question = None
    for question in PYTHON_QUESTION_LIST:
        if question['id'] == current_question_id:
            current_question = question
            break
    
    if not current_question:
        return False, "Current question not found"

    # Perform validation of the user's answer
    expected_answer = current_question['correct_answer']
    if answer.strip().lower() != expected_answer.strip().lower():
        return False, "Incorrect answer. Please try again."

    # Store the validated answer in the session
    session['answers'][current_question_id] = answer.strip()
    session.modified = True  # Ensure the session is marked as modified
    
    return True, ""



def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''

    return "dummy question", -1


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''

    return "dummy result"
