
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
    current_question = PYTHON_QUESTION_LIST[current_question_id]
    correct_answer = current_question['answer']

    if answer.lower() == correct_answer.lower():
        session['score'] = session.get('score', 0) + 1
        return True, "Correct!"
    else:
        return False, f"Sorry, the correct answer is {correct_answer}."


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    if current_question_id < len(PYTHON_QUESTION_LIST) - 1:
        next_question_id = current_question_id + 1
        next_question = PYTHON_QUESTION_LIST[next_question_id]['question']
        return next_question, next_question_id
    else:
        return None, -1



def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    score = session.get('score', 0)
    total_questions = len(PYTHON_QUESTION_LIST)
    percentage = (score / total_questions) * 100

    if percentage >= 80:
        result_message = "Congratulations! You scored {}% and passed the quiz!".format(percentage)
    else:
        result_message = "Sorry, you scored {}% and didn't pass the quiz. Better luck next time!".format(percentage)

    return result_message
