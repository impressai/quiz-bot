
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


from .constants import PYTHON_QUESTION_LIST

def generate_final_response(session):
   
    # Collect all answers from the session
    total_questions = len(PYTHON_QUESTION_LIST)
    answers = {key: value for key, value in session.items() if key.startswith("answer_")}

    # Calculate the number of questions answered
    questions_answered = len(answers)
    correctly_answered = 0  # Replace with actual correctness logic if available

    # Example correctness logic (can be expanded with actual validation)
    for key, answer in answers.items():
        # Example: treat non-empty answers as correct for simplicity
        if answer.strip():
            correctly_answered += 1

    # Calculate performance percentage
    performance_percentage = (correctly_answered / total_questions) * 100

    # Generate final message
    result_message = (
        f"Quiz Completed!\n"
        f"Total Questions: {total_questions}\n"
        f"Questions Answered: {questions_answered}\n"
        f"Correct Answers: {correctly_answered}\n"
        f"Your Performance: {performance_percentage:.2f}%\n"
    )

    # Add feedback based on performance
    if performance_percentage == 100:
        result_message += "Excellent work! You got everything right. 🎉"
    elif performance_percentage >= 75:
        result_message += "Great job! Keep up the good work. 😊"
    elif performance_percentage >= 50:
        result_message += "Good effort! Practice more to improve further. 👍"
    else:
        result_message += "Don't give up! Review the material and try again. 💪"

    return result_message

