from flask import Flask, render_template, jsonify, request, redirect, url_for
import requests

app = Flask(__name__)

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

def get_stock_data(ticker):
    url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/prev?apiKey={'vAycONtalDFVJ6kECb9UcK7FBD7MWwpY'}"
    response = requests.get(url)
    return response.json()


@app.route('/quiz/<int:level>')
def quiz(level):
    level_to_ticker = {
        1: "MSFT"
    }
    ticker = level_to_ticker.get(level, "GOOGL")

    url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/prev?apiKey={'vAycONtalDFVJ6kECb9UcK7FBD7MWwpY'}"
    response = requests.get(url)
    data = response.json()

    # the returned JSON structure has the last price in a field named 'close'
    stock_price = data['results'][0]['c']

    question = f"What is the current price of {ticker}'s stock?"

    return render_template('quiz.html', level=level, stock_price=stock_price, question=question)

@app.route('/quiz_result/<int:level>', methods=['POST'])
def quiz_result(level):
    chosen_value = request.form['quiz_choice']
    #correct_choice = 'choice2'

    correct_answer = "correct answer"
    return render_template('quiz_result.html', chosen_value=chosen_value, correct_answer=correct_answer, level=level)

if __name__ == '__main__':
    app.run(debug=True)