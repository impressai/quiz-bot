from django.http import HttpResponse
from django.shortcuts import render

from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id",0)
    if message == '':
        bot_responses.append(BOT_WELCOME_MESSAGE)
        current_question_id = 0
    else:
        success, error = record_current_answer(message, current_question_id, session)
        if not success:
            return [error]

    # if not current_question_id==1:
    #     bot_responses.append(BOT_WELCOME_MESSAGE)




    next_question,next_options, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
        bot_responses.append("Options: " + ", ".join(next_options))
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


# Assuming the following structure for the questions


def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to the Django session.
    '''
    print(f"current_question_id received: {current_question_id}")
    if current_question_id == -1:
        current_question_id = 0
    if current_question_id is None:
        return False, "Invalid question ID. Question ID cannot be None."


    # Check if current_question_id is valid
    if current_question_id < 0 or current_question_id >= len(PYTHON_QUESTION_LIST):
        return False, "Invalid question ID."

    # Get correct answer
    correct_answer = PYTHON_QUESTION_LIST[current_question_id]["answer"]

    # Save user answer in the session
    user_answers = session.get("user_answers", {})
    user_answers[current_question_id] = answer
    session["user_answers"] = user_answers

    # Check if the answer matches the correct answer (case-insensitive)
    if answer.strip().lower() == correct_answer.strip().lower():
        session.save()  # Explicitly save session after modification
        return True, ""  # Correct answer
    else:
        session.save()  # Explicitly save session after modification
        return False, f"Wrong answer! The correct answer was: {correct_answer}"




def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    if current_question_id is None or not isinstance(current_question_id, int):
        current_question_id = 0
    if current_question_id + 1 < len(PYTHON_QUESTION_LIST):
        next_question = PYTHON_QUESTION_LIST[current_question_id + 1]["question_text"]
        next_options = PYTHON_QUESTION_LIST[current_question_id + 1]["options"]
        next_question_id = current_question_id + 1
        return next_question,next_options, next_question_id
    else:
        # No more questions, return None and the current ID for the final response
        return None,None, 0


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    user_answers = session.get("user_answers", {})
    correct_answers = 0
    total_questions = len(PYTHON_QUESTION_LIST)
    # Check user's answers and compare with the correct answers
    for question_id, user_answer in user_answers.items():
        try:
            question_id=int(question_id)
            correct_answer = PYTHON_QUESTION_LIST[question_id]["answer"]
        except (ValueError,IndexError):
            correct_answer="Invalid question ID"
        if user_answer.lower() == correct_answer.lower():
            correct_answers += 1
        # Calculate score percentage
    score_percentage = (correct_answers / total_questions) * 100
    result = f"You answered {correct_answers} out of {total_questions} questions correctly ({score_percentage:.2f}%)."
    if score_percentage == 100:
        result += " Excellent work!"
    elif score_percentage >= 75:
        result += " Well done!"
    elif score_percentage >= 50:
        result += " Good effort, but you can improve!"
    else:
        result += " Keep trying, you'll get it next time!"

    return result

def start_quiz(request):
    """
    Start the quiz by displaying the first question or processing answers.
    """
    # If it's the first request, initialize the session
    if 'current_question_id' not in request.session:
        request.session['current_question_id'] = 0
        request.session['user_answers'] = {}
        # Get the user's message
    user_message = request.GET.get('message', '').strip()

        # Generate bot responses
    bot_responses = generate_bot_responses(user_message, request.session)
    print(bot_responses)

        # Render the quiz template with the bot responses
    return render(request, 'quiz.html', {'bot_responses': bot_responses})








