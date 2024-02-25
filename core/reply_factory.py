
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
    if not answer:
        return False, "Answer cannot be empty"
    
    # Store the answer in the session
    session[str(current_question_id) + '_answer'] = answer
    
    return True, "Answer recorded successfully"


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''

    # Iterate through the PYTHON_QUESTION_LIST
    for i, (question_id, question_text) in enumerate(PYTHON_QUESTION_LIST):
        # If the current_question_id is found
        if question_id == current_question_id:
            # If it's not the last question, return the next question
            if i < len(PYTHON_QUESTION_LIST) - 1:
                return PYTHON_QUESTION_LIST[i + 1]
            break

    # Return a dummy question and -1 as the question ID if the current_question_id is not found or is the last question
    return "dummy question", -1


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''

    total_questions = len(PYTHON_QUESTION_LIST)
    total_correct = 0

    # Iterate through the PYTHON_QUESTION_LIST and check if user's answer matches the expected answer
    for question_id, _ in PYTHON_QUESTION_LIST:
        # Retrieve the expected answer for the current question (assuming it's stored in session)
        expected_answer = session.get(str(question_id) + '_answer', None)
        if expected_answer is not None:
            # If the user's answer matches the expected answer, increment the total correct count
            user_answer = session.get(str(question_id), None)
            if user_answer == expected_answer:
                total_correct += 1

    # Calculate the score as a percentage of correct answers
    score_percentage = (total_correct / total_questions) * 100

    # Generate the final result message
    final_result_message = f"You scored {total_correct} out of {total_questions} questions correctly. Your score is {score_percentage:.2f}%."

    return final_result_message
