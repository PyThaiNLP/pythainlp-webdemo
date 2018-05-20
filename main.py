# -*- coding: utf-8 -*-
import logging
import platform

from flask import Flask


app = Flask(__name__)


@app.route('/')
def home():
    return "Hi"


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)