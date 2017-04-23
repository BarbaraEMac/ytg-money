import logging

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World!'

@app.errorhandler(500)
def server_error(e):
    #log the error and stacktrace
    logging.exception('An error occured during a request.')
    return 'An internal error occured.', 500
