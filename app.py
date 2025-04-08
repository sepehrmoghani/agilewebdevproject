from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("html/index.html")

@app.route('/login')
def login():
    return render_template('html/login.html')

@app.route('/signup')
def signup():
    return render_template('html/signup.html')

@app.route('/privacy')
def privacy():
    return render_template('html/privacy.html') 

@app.route('/feedback')
def feedback():
    return render_template('html/feedback.html') 

if __name__ == '__main__':
    app.run(debug=True)
