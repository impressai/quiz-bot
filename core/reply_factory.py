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
    if current_question_id is None or current_question_id < 0:
        return True, ""

    if current_question_id >= len(PYTHON_QUESTION_LIST):
        return False, "Invalid question ID"

    current_question = PYTHON_QUESTION_LIST[current_question_id]

    if "answers" not in session:
        session["answers"] = {}

    session["answers"][str(current_question_id)] = {
        "user_answer": answer,
        "is_correct": answer == current_question["answer"],
    }

    return True, ""


def get_next_question(current_question_id):
    if current_question_id is None:
        next_question_id = 0
    else:
        next_question_id = current_question_id + 1

    if next_question_id >= len(PYTHON_QUESTION_LIST):
        return None, -1

    next_question = PYTHON_QUESTION_LIST[next_question_id]

    question_text = f"{next_question['question_text']}\n\n"
    question_text += "Options:\n"
    for i, option in enumerate(next_question["options"], 1):
        question_text += f"{i}. {option}\n"

    return question_text, next_question_id


def generate_final_response(session):
    user_answers = session.get("answers", {})
    total_questions = len(PYTHON_QUESTION_LIST)

    if not user_answers:
        return "You didn't answer any questions. Your score is 0/0 (0%)"

    correct_answers = sum(
        1 for q_id, answer in user_answers.items() if answer.get("is_correct", False)
    )
    score_percent = (correct_answers / total_questions) * 100

    response = [
        "\n=== Quiz Results ===\n",
        f"You answered {correct_answers} out of {total_questions} questions correctly ({score_percent:.1f}%).\n",
    ]

    if score_percent >= 80:
        response.append(" Excellent work! You have a strong understanding of Python!")
    elif score_percent >= 60:
        response.append(" Good job! You have a good grasp of Python fundamentals!")
    elif score_percent >= 40:
        response.append(" Not bad! Keep practicing to improve your Python skills!")
    else:
        response.append(
            " Keep learning! Everyone starts somewhere. Review the basics and try again!"
        )

    response.append("\n\n=== Question Review ===")
    for i, question in enumerate(PYTHON_QUESTION_LIST):
        answer = user_answers.get(str(i), {})
        user_answer = answer.get("user_answer", "No answer")
        is_correct = answer.get("is_correct", False)

        response.append(f"\nQ{i+1}. {question['question_text']}")
        response.append(f"Your answer: {user_answer}")
        if is_correct:
            response.append(" Correct!")
        else:
            response.append(f"Incorrect. The correct answer is: {question['answer']}")

    return "\n".join(response)
