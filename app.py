from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/quiz/<level>')
def quiz(level):
    return render_template('quiz.html', level=level)

@app.route('/api/stock_data')
def stock_data():
    response = requests.get("URL_TO_STOCK_API")
    data = response.json()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)