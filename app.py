from flask import Flask

app = Flask(__name__)
@app.route('/')

def hello_computer():
    return 'Go away!'