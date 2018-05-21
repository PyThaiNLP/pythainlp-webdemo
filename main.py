# -*- coding: utf-8 -*-
"""
PyThaiNLP Demo Online
V 0.1
พัฒนาโดย นาย วรรณพงษ์  ภัททิยไพบูลย์
"""
import logging
from flask import Flask, render_template, abort, request,jsonify
from pythainlp.tokenize import word_tokenize
from pythainlp.tokenize import tcc
#from pythainlp.word_vector import thai2vec
from pythainlp.tag import pos_tag
from pythainlp.sentiment import sentiment
from pythainlp.soundex import LK82,Udom83
import json
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', name='Home')

@app.route('/word_tokenizer')
def word_tokenizer_web():
    return render_template('word_tokenizer.html', name='Word tokenizer')

@app.route('/pos_tag')
def pos_tag_web():
    return render_template('pos_tag.html', name='POS Tag')

@app.route('/thai2vec')
def thai2vec_web():
    return render_template('thai2vec.html', name='Thai2Vec')

@app.route('/api/word_tokenizer', methods=["GET"])
def word_tokenizer_api():
	sent = request.args.get('sent', 0, type=str)
	txt='|'.join(word_tokenize(sent)).replace('|<|br|>','<br>')
	return jsonify(result=txt)

@app.route('/api/pos_tag', methods=["GET"])
def pos_tag_api():
	sent = request.args.get('sent', 0, type=str)
	txt=" ".join("%s/%s" % tup for tup in pos_tag(word_tokenize(sent),engine='artagger'))
	return jsonify(result=txt)


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)