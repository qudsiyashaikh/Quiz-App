
from flask import Flask, render_template_string, request, session, redirect

app = Flask(__name__)
app.secret_key = 'quiz_secret_key'

# Lists & Dictionaries Concepts: Storing the MCQ database
QUESTIONS = [
    {
        "id": 0,
        "question": "What is the correct file extension for Python files?",
        "options": [".pt", ".py", ".pyt", ".pyw"],
        "correct": ".py"
    },
    {
        "id": 1,
        "question": "Which keyword is used to create a function in Python?",
        "options": ["function", "void", "def", "func"],
        "correct": "def"
    },
    {
        "id": 2,
        "question": "Which data type is used to store multiple items in a single variable ordered and changeable?",
        "options": ["List", "Tuple", "Set", "Dictionary"],
        "correct": "List"
    },
    {
        "id": 3,
        "question": "What is the output of: print(2 ** 3)?",
        "options": ["6", "8", "9", "5"],
        "correct": "8"
    },
    {
        "id": 4,
        "question": "Which of the following is a mutable data type in Python?",
        "options": ["Tuple", "String", "List", "Integer"],
        "correct": "List"
    },
    {
        "id": 5,
        "question": "What is the output of print(type([]) ) in Python?",
        "options": ["<class 'dict'>", "<class 'tuple'>", "<class 'set'>", "<class 'list'>"],
        "correct": "<class 'list'>"
    },
    {
        "id": 6,
        "question": "Which symbol is used to write comments in Python?",
        "options": ["//", "#", "/*", "<!-- -->"],
        "correct": "#"
    },
    {
        "id": 7,
        "question": "What will be the output of 3 * 3 in Python?",
        "options": ["6", "9", "27", "33"],
        "correct": "9"
    },
    {
        "id": 8,
        "question": "Which collection does not allow duplicate members?",
        "options": ["List", "Tuple", "Set", "None of these"],
        "correct": "Set"
    },
    {
        "id": 9,
        "question": "Which of the following is a correct dictionary definition?",
        "options": ["x = ['a': 1]", "x = {'a': 1}", "x = ('a': 1)", "x = 'a': 1"],
        "correct": "x = {'a': 1}"
    }
    
]

# --- HTML & CSS TEMPLATE ---
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Python MCQ Quiz</title>
    <style>
        body { font-family: Arial, sans-serif; background: #ebf5fb; text-align: center; margin-top: 50px; }
        .container { display: inline-block; padding: 30px; background: white; border-radius: 10px; box-shadow: 0px 0px 15px rgba(0,0,0,0.1); width: 500px; text-align: left; }
        h2 { text-align: center; color: #2e4053; }
        .options-label { display: block; background: #f2f4f4; padding: 12px; margin: 8px 0; border-radius: 5px; cursor: pointer; border: 1px solid #d5dbdb; }
        .options-label:hover { background: #e5e8e8; }
        input[type="radio"] { margin-right: 10px; }
        button { width: 100%; background-color: #2e86c1; color: white; border: none; padding: 12px; font-size: 16px; font-weight: bold; border-radius: 5px; cursor: pointer; margin-top: 15px; }
        button:hover { background-color: #21618c; }
        .score-box { text-align: center; font-size: 22px; font-weight: bold; color: #196f3d; }
        .feedback { font-weight: bold; margin-bottom: 15px; font-size: 16px; padding: 10px; border-radius: 5px; }
        .correct { background-color: #d4edda; color: #155724; }
        .wrong { background-color: #f8d7da; color: #721c24; }
    </style>
</head>
<body>

<div class="container">
    <h2>📝 Python MCQ Quiz</h2>
    <hr>

    {% if quiz_over %}
        <div class="score-box">
            <p>Quiz Finished! 🎉</p>
            <p>Your Score: {{ score }} / {{ total }}</p>
        </div>
        <form method="POST" action="/reset">
            <button type="submit">Restart Quiz</button>
        </form>
    {% else %}
        {% if feedback %}
            <div class="feedback {{ feedback_class }}">{{ feedback }}</div>
        {% endif %}

        <h3>Question {{ current_index + 1 }}:</h3>
        <p style="font-size: 18px;">{{ question_data.question }}</p>

        <form method="POST" action="/submit">
            {% for option in question_data.options %}
                <label class="options-label">
                    <input type="radio" name="user_answer" value="{{ option }}" required> {{ option }}
                </label>
            {% endfor %}
            <button type="submit">Submit Answer</button>
        </form>
    {% endif %}
</div>

</body>
</html>
"""

@app.route('/')
def home():
    if 'current_index' not in session:
        session['current_index'] = 0
        session['score'] = 0
        session['feedback'] = ""
        session['feedback_class'] = ""

    current_index = session['current_index']
    quiz_over = current_index >= len(QUESTIONS)

    return render_template_string(
        HTML,
        quiz_over=quiz_over,
        score=session.get('score', 0),
        total=len(QUESTIONS),
        current_index=current_index,
        question_data=QUESTIONS[current_index] if not quiz_over else None,
        feedback=session.get('feedback', ""),
        feedback_class=session.get('feedback_class', "")
    )

@app.route('/submit', methods=['POST'])
def submit_answer():
    user_ans = request.form.get('user_answer')
    current_index = session.get('current_index', 0)
    
    correct_ans = QUESTIONS[current_index]['correct']
    
    # Conditions Concept: Evaluation of right or wrong choices
    if user_ans == correct_ans:
        session['score'] += 1
        session['feedback'] = "Correct Answer! ✔️"
        session['feedback_class'] = "correct"
    else:
        session['feedback'] = f"Wrong Answer! ❌ (Correct answer was: {correct_ans})"
        session['feedback_class'] = "wrong"
        
    session['current_index'] += 1
    return redirect('/')

@app.route('/reset', methods=['POST'])
def reset_quiz():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)