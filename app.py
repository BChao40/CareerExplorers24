from flask import Flask, render_template, jsonify, request, redirect, url_for
import requests
from vocabulary import vocabulary
from questions import questions

app = Flask(__name__)

def get_stock_data(ticker):
    url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/prev?apiKey={'vAycONtalDFVJ6kECb9UcK7FBD7MWwpY'}"
    response = requests.get(url)
    return response.json()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/resources')
def resources():
    if request.method == 'POST':
        ticker = request.form['ticker']
        return redirect(url_for('stock_data/<ticker>', ticker=ticker))
    return render_template('resources.html')

@app.route('/stock_data/<ticker>')
def stock_data(ticker):
    stock_info = get_stock_data(ticker)['results'][0]
    if stock_info:
        return render_template('stock_data.html', stock=stock_info, ticker=ticker)
    else:
        return "Error fetching data", 500

@app.route('/quiz/<int:level>')
def quiz(level):
    question = next((q for q in questions if q["level"] == level), None)
    
    if not question:
        return "No question found for this level", 404
    
    if question["type"] == "stock_price":
        ticker = question["ticker"]
        stock_info = get_stock_data(ticker)
        if stock_info:
            price = stock_info['results'][0]['c']
            question_text = question["question"].replace("{ticker}", ticker)
            answers = [{"text": answer["text"].replace("{price}", str(price)), "correct": answer["correct"]} for answer in question["answers"]]
            print(f"Ticker: {ticker}")
            print(f"Answers: {answers}")
        else:
            return "Error fetching stock data", 500
    else:
        question_text = question["question"]
        answers = question["answers"]
        print(f"Question: {question_text}")
        print(f"Answers: {answers}")
    
    return render_template('quiz.html', level=level, question=question_text, answers=answers, question_type=question["type"])

@app.route('/quiz_result/<int:level>', methods=['POST'])
def quiz_result(level):
    question = next((q for q in questions if q["level"] == level), None)
    
    if not question:
        return "No question found for this level", 404
    
    if question["type"] in ["stock_price", "multiple_choice", "true_false"]:
        chosen_value = request.form['quiz_choice']
        correct = next((answer for answer in question["answers"] if answer["text"] == chosen_value), {}).get("correct", False)
        explanation = question["explanation"]
        feedback = "Correct! " + explanation if correct else "Incorrect. " + explanation
    elif question["type"] == "text":
        user_answer = request.form['quiz_answer']
        explanation = question["explanation"]
        feedback = "Sample response: " + explanation

    return render_template('quiz_result.html', feedback=feedback, level=level)

@app.route('/vocabulary')
def vocabulary_page():
    return render_template('vocabulary.html', vocabulary=vocabulary)

if __name__ == '__main__':
    app.run(debug=True)