
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
    return True, ""


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''

    return "dummy question", -1


def generate_final_response(session):
    """
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    """
    from .constants import PYTHON_QUESTION_LIST  # Import the question list if not already imported
    
    answers = session.get('answers', {})  # Retrieve answers stored in session
    total_questions = len(PYTHON_QUESTION_LIST)
    correct_answers_count = 0
    
    # Calculate number of correct answers
    for question in PYTHON_QUESTION_LIST:
        question_id = question['id']
        if question_id in answers:
            user_answer = answers[question_id]
            expected_answer = question['correct_answer']
            if user_answer.strip().lower() == expected_answer.strip().lower():
                correct_answers_count += 1
    
    # Calculate performance based on correct answers
    score = (correct_answers_count / total_questions) * 100
    
    # Generate final response message based on performance
    if score >= 70:
        final_response = f"Congratulations! You scored {score}% and passed the quiz."
    else:
        final_response = f"Sorry, you scored {score}%. Please review and try again."
    
    return final_response
