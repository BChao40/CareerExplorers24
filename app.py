from flask import Flask, render_template, jsonify, redirect, url_for
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/resources')
def resources():
    return render_template('resources.html')

@app.route('/quiz/<level>')
def quiz(level):
    return render_template('quiz.html', level=level)

@app.route('/api/stock_data/ticker')
def stock_data(ticker):
    response = requests.get(f"https://api.polygon.io/v2/aggs/ticker/{ticker}/prev?apiKey={vAycONtalDFVJ6kECb9UcK7FBD7MWwpY}") # url goes here
    data = response.json()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)