
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
    if current_question_id is None:
        return False, "No question is currently active."
    if not answer or not answer.strip():
        return False, "The answer cannot be empty. Please provide a valid response."
    session[f"answer_{current_question_id}"] = answer.strip()
    return True, ""

def get_next_question(current_question_id):
    if current_question_id is None:
        return PYTHON_QUESTION_LIST[0], 0
    next_question_id = current_question_id + 1
    if next_question_id < len(PYTHON_QUESTION_LIST):
        return PYTHON_QUESTION_LIST[next_question_id], next_question_id
    return None, None

def generate_final_response(session):
    total_questions = len(PYTHON_QUESTION_LIST)
    answers = {key: value for key, value in session.items() if key.startswith("answer_")}
    questions_answered = len(answers)
    correctly_answered = 0

    for key, answer in answers.items():
        if answer.strip():
            correctly_answered += 1

    performance_percentage = (correctly_answered / total_questions) * 100

    result_message = (
        f"Quiz Completed!\n"
        f"Total Questions: {total_questions}\n"
        f"Questions Answered: {questions_answered}\n"
        f"Correct Answers: {correctly_answered}\n"
        f"Your Performance: {performance_percentage:.2f}%\n"
    )

    if performance_percentage == 100:
        result_message += "Excellent work! You got everything right. 🎉"
    elif performance_percentage >= 75:
        result_message += "Great job! Keep up the good work. 😊"
    elif performance_percentage >= 50:
        result_message += "Good effort! Practice more to improve further. 👍"
    else:
        result_message += "Don't give up! Review the material and try again. 💪"

    return result_message

