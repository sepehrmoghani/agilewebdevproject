from flask import Flask, render_template
from app import create_app
from app.authentication import authentication_bp

app = create_app()

@app.route('/')
def home():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
