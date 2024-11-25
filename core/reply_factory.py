from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST

# Assuming the 'correct_answers_dict' is defined somewhere to map questions to correct answers.
# For now, we'll initialize it as a dummy dictionary for demonstration.
correct_answers_dict = {
    0: "Python",  # Example, question_id 0's correct answer is 'Python'
    1: "Django"   # Example, question_id 1's correct answer is 'Django'
}

def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    
    if not current_question_id:
        # Start the quiz, send a welcome message.
        bot_responses.append(BOT_WELCOME_MESSAGE)
        session["current_question_id"] = 0  # Start from the first question
        session["answers"] = {}  # Initialize an empty dictionary to store answers
        session.save()

    # Record the user's answer for the current question
    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    # Get the next question to ask the user
    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        # If no more questions, generate the final response with the score
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    # Update session with the next question ID
    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to Django session.
    '''
    if not answer.strip():  # Validate answer: check if not empty
        return False, "Answer cannot be empty."

    # Store the user's answer in session
    session["answers"][current_question_id] = answer.strip()
    return True, ""


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    next_question_id = current_question_id + 1
    if next_question_id < len(PYTHON_QUESTION_LIST):
        return PYTHON_QUESTION_LIST[next_question_id], next_question_id
    else:
        return None, -1  # No more questions, return -1


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    total_questions = len(PYTHON_QUESTION_LIST)
    correct_answers = 0

    # Compare stored answers to the correct answers
    for question_id, user_answer in session["answers"].items():
        correct_answer = correct_answers_dict.get(question_id)
        if user_answer.lower() == correct_answer.lower():  # Case-insensitive comparison
            correct_answers += 1

    # Calculate the score as a percentage
    score = (correct_answers / total_questions) * 100
    return f"Your final score is: {score:.2f}%"
