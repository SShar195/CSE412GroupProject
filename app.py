from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/movie_info.html')
def movie_info():
    # You can pass movie data dynamically here if needed
    return render_template('movie_info.html')

if __name__ == '__main__':
    app.run(debug=True)
