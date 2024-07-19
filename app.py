from flask import Flask, render_template, jsonify, redirect, url_for
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/resources')
def resources():
    return render_template('resources.html')

@app.route('/quiz/<int:level>')
def quiz(level):
    level_to_ticker = {
        1: "GOOGL"
    }
    ticker = level_to_ticker.get(level, "GOOGL")

    url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/prev?apiKey={'vAycONtalDFVJ6kECb9UcK7FBD7MWwpY'}"
    response = requests.get(url)
    data = response.json()

    # the returned JSON structure has the last price in a field named 'close'
    stock_price = data['results'][0]['c']

    question = f"What is the current price of {ticker}'s stock, and what could be a potential future value?"

    return render_template('quiz.html', level=level, stock_price=stock_price, question=question)

@app.route('/quiz_result/<int:level>', methods=['POST'])
def quiz_result(level):
    chosen_value = request.form['stock_choice']
    correct_choice = 'choice2'

    # if chosen_value == correct_choice:
        # +1 score, +1 total
    # else:
        # +0 score, +1 total

    correct_answer = "correct answer"
    return render_template('quiz_result.html', chosen_value=chosen_value, correct_answer=correct_answer, level=level)

@app.route('/api/stock_data/ticker')
def stock_data(ticker):
    response = requests.get(f"https://api.polygon.io/v2/aggs/ticker/{ticker}/prev?apiKey={'vAycONtalDFVJ6kECb9UcK7FBD7MWwpY'}")
    data = response.json()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)