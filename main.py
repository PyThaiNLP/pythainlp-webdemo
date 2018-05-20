# -*- coding: utf-8 -*-
"""
PyThaiNLP Demo Online
V 0.1
พัฒนาโดย นาย วรรณพงษ์  ภัททิยไพบูลย์
"""
import logging
from flask import Flask
from pythainlp.tokenize import word_tokenize
from pythainlp.tokenize import tcc
from pythainlp.word_vector import thai2vec
from pythainlp.tag import pos_tag
from pythainlp.sentiment import sentiment
from pythainlp.soundex import LK82,Udom83
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