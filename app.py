from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('homepage.html')

if __name__ == '__main__':
    app.run(debug=True)