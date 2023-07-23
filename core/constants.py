
BOT_WELCOME_MESSAGE = "Hello, I'm Quizbot. I'll asking you a few questions to assess your python programming skils."

PYTHON_QUESTION_LIST = [
    {
      "question_text": "What is the output of the following code?\n\nx = 5\ny = 2\nprint(x + y)",
      "options": ["7", "52", "3", "5+2"],
      "answer": "7",
    },
    {
      "question_text": "Which of the following is NOT a valid Python variable name?",
      "options": ["my_var", "1var", "_var", "Var_2"],
      "answer": "1var",
    },
    {
      "question_text": "What does the 'len()' function do in Python?",
      "options": ["Converts a string to lowercase", "Returns the number of items in a list", "Finds the maximum value in a list", "Converts a number to a string"],
      "answer": "Returns the number of items in a list",
    },
    {
      "question_text": "Which of the following is used to comment a single line in Python?",
      "options": ["# Comment", "// Comment", "/* Comment */", "<!-- Comment -->"],
      "answer": "# Comment",
    },
    {
      "question_text": "What does the 'range()' function return?",
      "options": ["A list of integers", "A string", "A float number", "An iterator"],
      "answer": "An iterator",
    },
    {
      "question_text": "What is the correct way to open a file named 'data.txt' in read mode?",
      "options": ["file.open('data.txt', 'r')", "open('data.txt', 'read')", "open('data.txt', 'r')", "file.open('data.txt', 'read')"],
      "answer": "open('data.txt', 'r')",
    },
    {
      "question_text": "Which of the following is used to remove an item from a list?",
      "options": ["delete()", "remove()", "discard()", "pop()"],
      "answer": "pop()",
    },
    {
      "question_text": "What is the result of the expression '3' + '4'?",
      "options": ["34", "7", "12", "Error"],
      "answer": "34",
    },
    {
      "question_text": "In Python, which module is used to work with dates and times?",
      "options": ["datetime", "time", "date", "calendar"],
      "answer": "datetime",
    },
    {
      "question_text": "What is the output of the following code?\n\nx = [1, 2, 3]\ny = x\nx.append(4)\nprint(y)",
      "options": ["[1, 2, 3, 4]", "[1, 2, 3]", "[1, 2, 3, 4, 4]", "Error"],
      "answer": "[1, 2, 3, 4]",
    }
  ]