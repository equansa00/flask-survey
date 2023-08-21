from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = "some_secret_key"  # Necessary for session and flash messages

# This would be imported from your surveys.py
from surveys import satisfaction_survey

@app.route('/')
def show_survey_start():
    return render_template('start.html', survey=satisfaction_survey)

@app.route('/questions/<int:id>')
def show_question(id):
    # Check if the user tries to access a question out of order
    if id != len(session.get('responses', [])):
        flash('You are trying to access an invalid question.')
        return redirect(f"/questions/{len(session.get('responses', []))}")
    
    question = satisfaction_survey.questions[id]
    return render_template('question.html', question=question)

@app.route('/answer', methods=['POST'])
def handle_answer():
    responses = session.get('responses', [])
    answer = request.form['choice']
    responses.append(answer)
    session['responses'] = responses  # Update session data
    
    if len(responses) < len(satisfaction_survey.questions):
        return redirect(f"/questions/{len(responses)}")
    return redirect('/thankyou')

@app.route('/thankyou')
def thank_you():
    return "Thank You!"

# For running the application
if __name__ == "__main__":
    app.run(debug=True)
