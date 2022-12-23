from flask import Flask, render_template
from random import choice

app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)