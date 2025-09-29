from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if current_question_id is None:
        # First interaction: send welcome and first question
        bot_responses.append(BOT_WELCOME_MESSAGE)
        next_question, next_question_id = get_next_question(None)
        if next_question:
            bot_responses.append(next_question)
            session["current_question_id"] = next_question_id
            session.save()
        return bot_responses

    # Otherwise, process answer and move to next question
    success, error = record_current_answer(message, current_question_id, session)
    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)
    if next_question:
        bot_responses.append(next_question)
        session["current_question_id"] = next_question_id
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)
        session["current_question_id"] = None  # Reset for next quiz

    session.save()
    return bot_responses


def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to django session.
    '''
    # Validate that there is a current question
    if current_question_id is None or current_question_id < 0:
        return False, "No active question to answer."

    # Get the question list
    questions = PYTHON_QUESTION_LIST
    if current_question_id >= len(questions):
        return False, "Invalid question ID."

    # Get the correct answer for the current question
    correct_answer = questions[current_question_id].get("answer")
    if correct_answer is None:
        return False, "Question data is incomplete."

    # Store the user's answer in the session
    user_answers = session.get("user_answers", {})
    user_answers[current_question_id] = answer.strip()
    session["user_answers"] = user_answers

    if not answer.strip():
        return False, "Answer cannot be empty."

    return True, ""


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    Returns the question text and the next question's id.
    '''
    questions = PYTHON_QUESTION_LIST
    if current_question_id is None:
        next_id = 0
    else:
        next_id = current_question_id + 1

    if next_id < len(questions):
        q = questions[next_id]
        # Show options if available
        options = q.get("options")
        question_text = q.get("question_text", "No question text available.")
        if options:
            question_text += "\nOptions: " + ", ".join(options)
        return question_text, next_id
    else:
        return None, None  # No more questions


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    questions = PYTHON_QUESTION_LIST
    user_answers = session.get("user_answers", {})
    score = 0
    total = len(questions)
    details = []

    for idx, q in enumerate(questions):
        correct = q.get("answer", "").strip().lower()
        user = user_answers.get(idx, "").strip().lower()
        if user == correct:
            score += 1
            details.append(f"Q{idx+1}: Correct")
        else:
            details.append(f"Q{idx+1}: Incorrect (Your answer: '{user}', Correct: '{correct}')")

    result = f"Quiz complete! Your score: {score} out of {total}."
    details.append(result)
    return "\n".join(details)
