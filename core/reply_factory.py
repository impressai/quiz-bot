
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if current_question_id is None:
        current_question_id = 0
        session["current_question_id"] = current_question_id
        session.save()

    print(type(current_question_id), current_question_id)
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(
        message, current_question_id, session)

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
    Validates and stores the answer for the current question to Django session.
    '''
    if current_question_id is None:
        return False, "No active question found."

    if current_question_id >= len(PYTHON_QUESTION_LIST):
        return False, "Invalid question ID."

    user_answers = session.get("message_history", [])

    if not isinstance(user_answers, list):
        user_answers = []

    # Store answer in lowercase as a dictionary inside the list
    user_answers.append({str(current_question_id): answer.strip().lower()})

    session["message_history"] = user_answers
    session.save()

    return True, ""


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    next_question_id = current_question_id + 1

    if next_question_id < len(PYTHON_QUESTION_LIST):
        question_data = PYTHON_QUESTION_LIST[next_question_id]
        question_text = f"{question_data['question_text']}\nOptions: {', '.join(question_data['options'])}"
        return question_text, next_question_id

    return False, -1


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    user_answers = session.get("message_history", [])
    score = 0

    for answer_dict in user_answers:
        if not isinstance(answer_dict, dict):
            continue

        for q_id, user_answer in answer_dict.items():
            if not q_id.isdigit():
                continue

            q_id = int(q_id)
            correct_answer = PYTHON_QUESTION_LIST[q_id]["answer"].strip(
            ).lower()

            if user_answer.strip().lower() == correct_answer:
                score += 1

    total_questions = len(PYTHON_QUESTION_LIST)
    return f"Quiz completed! Your final score is {score}/{total_questions}."
