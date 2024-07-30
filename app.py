from flask import Flask, render_template, jsonify, request, redirect, url_for
import requests
from vocabulary import vocabulary
from questions import questions

app = Flask(__name__)

def get_stock_data(ticker):
    url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/prev?apiKey={'vAycONtalDFVJ6kECb9UcK7FBD7MWwpY'}"
    response = requests.get(url)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response Content: {response.content}")

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 429:  #429 too many api requests
        return {"error": "rate_limit_exceeded"}
    else:
        return {"error": "api_error"}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/resources', methods=['GET', 'POST'])
def resources():
    if request.method == 'POST':
        ticker = request.form['ticker']
        return redirect(url_for('stock_data', ticker=ticker))
    return render_template('resources.html')

@app.route('/stock_data/<ticker>')
def stock_data(ticker):
    stock_info = get_stock_data(ticker)
    
    if "error" in stock_info:
        if stock_info["error"] == "rate_limit_exceeded":
            return render_template('rate_limit_exceeded.html')
        else:
            return "Error fetching data", 500
    
    if stock_info and 'results' in stock_info and len(stock_info['results']) > 0:
        return render_template('stock_data.html', stock=stock_info['results'][0], ticker=ticker)
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
        
        if "error" in stock_info:
            if stock_info["error"] == "rate_limit_exceeded":
                return render_template('rate_limit_exceeded.html')
            else:
                return "Error fetching stock data", 500
        
        if stock_info and 'results' in stock_info and len(stock_info['results']) > 0:
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
    
    print(f"Received POST data: {request.form}") 

    if str(request.form) == "ImmutableMultiDict([])":
        error_message = "Please select an answer."
        print(f"Error: {error_message}")
        return render_template('quiz.html', level=level, question=question["question"], answers=question["answers"], question_type=question["type"], error_message=error_message)
    
    if question["type"] in ["stock_price", "multiple_choice", "true_false"]:
        chosen_value = request.form.get('quiz_choice')
        
        if question["type"] == "stock_price":
            stock_info = get_stock_data(question["ticker"])
            
            if "error" in stock_info:
                if stock_info["error"] == "rate_limit_exceeded":
                    return render_template('rate_limit_exceeded.html')
                else:
                    return "Error fetching stock data", 500
            
            if stock_info and 'results' in stock_info and len(stock_info['results']) > 0:
                price = stock_info['results'][0]['c']
                correct = next((answer for answer in question["answers"] if answer["text"].replace("{price}", str(price)) == chosen_value), {}).get("correct", False)
            else:
                return "Error fetching stock data", 500
        else:
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

@app.route('/level_select')
def level_select():
    return render_template('level_select.html', questions=questions)

if __name__ == '__main__':
    app.run(debug=True)