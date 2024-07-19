
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


def record_current_answer(user_response, correct_answer, user_data):
    # Validate the user's response
    if user_response.lower() == correct_answer.lower():
        user_data['score'] += 1

    # Store the user's answer
    user_data['answers'].append(user_response)
    
    return user_data


def get_next_question(questions, current_question_index):
    # Check if there are more questions to ask
    if current_question_index < len(questions):
        return questions[current_question_index], current_question_index + 1
    else:
        return None, current_question_index


def generate_final_response(user_data):
    total_questions = len(user_data['answers'])
    score = user_data['score']

    response = f"You've completed the quiz! Your score is {score}/{total_questions}."
    return response
