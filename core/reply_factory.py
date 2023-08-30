
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
    # Validate the answer (add your validation logic here)
    if answer is None or answer == "":
        return False, "Answer cannot be empty."

    # Store the answer in the Django session
    session["answers"][current_question_id] = answer

    return True, ""
    


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''

    PYTHON_QUESTION_LIST = [
        {'question_id': 1, 'question_text': 'Question 1'},
        {'question_id': 2, 'question_text': 'Question 2'},
        {'question_id': 3, 'question_text': 'Question 3'},
        # Add more questions as needed
    ]

    # Check if the current_question_id is within the valid range
    if current_question_id < 0 or current_question_id >= len(PYTHON_QUESTION_LIST):
        return None, -1  # Return None and -1 to indicate no more questions

    # Fetch the next question based on the current_question_id
    next_question = PYTHON_QUESTION_LIST[current_question_id]

    return next_question, current_question_id + 1


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''

     # Define the PYTHON_QUESTION_LIST
    PYTHON_QUESTION_LIST = [
        {'question_id': 1, 'question_text': 'Question 1', 'correct_answer': 'A'},
        {'question_id': 2, 'question_text': 'Question 2', 'correct_answer': 'B'},
        {'question_id': 3, 'question_text': 'Question 3', 'correct_answer': 'C'},
        # Add more questions as needed
    ]

    # Initialize the score
    score = 0

    # Iterate over the questions and check the user's answers
    for question in PYTHON_QUESTION_LIST:
        question_id = question['question_id']
        correct_answer = question['correct_answer']

        # Check if the user answered this question
        if question_id in session['answers']:
            user_answer = session['answers'][question_id]

            # Check if the user's answer is correct
            if user_answer == correct_answer:
                score += 1

    # Create the final result message
    result_message = f"Your score is {score}/{len(PYTHON_QUESTION_LIST)}."

    return result_message
