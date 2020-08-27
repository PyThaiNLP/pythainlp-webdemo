# -*- coding: utf-8 -*-
"""
PyThaiNLP Demo Online
V 0.1
พัฒนาโดย นาย วรรณพงษ์  ภัททิยไพบูลย์
"""
import logging
import json
import os

from flask import Flask, render_template, abort, request, jsonify
from flask import redirect, url_for

from datetime import datetime

import pythainlp
from pythainlp.tokenize import word_tokenize
from pythainlp.tokenize import tcc, syllable_tokenize
from pythainlp.tag import pos_tag
from pythainlp.tag.named_entity import ThaiNameTagger
from pythainlp.soundex import lk82, udom83

import yaml

with open("./config.yaml", 'r') as stream:
    app_config = yaml.safe_load(stream)

port = os.environ.get("PORT", 80)

app = Flask(__name__)

@app.route('/')
def home():
	return redirect(url_for('word_tokenizer_web'))

@app.route('/word_tokenizer')
def word_tokenizer_web():
    return render_template('word_tokenizer.html', name='Word tokenizer')

@app.route('/pos_tag')
def pos_tag_web():
    return render_template('pos_tag.html', name='POS Tag')

@app.route('/ner')
def ner_web():
    return render_template('ner.html', name='NER')

@app.route('/thai2vec')
def thai2vec_web():
    return render_template('thai2vec.html', name='Thai2Vec')

@app.route('/soundex')
def soundex_web():
    return render_template('soundex.html', name='Soundex')

@app.route('/tcc')
def tcc_web():
    return render_template('tcc.html', name='TCC')

@app.route('/syllable')
def syllable_web():
    return render_template('syllable.html', name='Syllable')

@app.route('/api/word_tokenizer', methods=["GET"])
def word_tokenizer_api():

	sent = request.args.get('sent', 0, type=str)
	engine = request.args.get('engine', 0, type=str)

	tokenised = word_tokenize(sent, engine=engine)
	
	return jsonify(result='|'.join(tokenised))

@app.route('/api/tcc', methods=["GET"])
def tcc_api():
	txt = request.args.get('sent', 0, type=str)
	res = "~".join(tcc.tcc(txt.strip()))
	return jsonify(result=res)

@app.route('/api/syllable', methods=["GET"])
def syllable_api():
	txt = request.args.get('sent', 0, type=str)
	res = "~".join(syllable_tokenize(txt.strip()))
	return jsonify(result=res)

@app.route('/api/ner', methods=["GET"])
def ner_api():
	ner = ThaiNameTagger()
	txt = request.args.get('sent', 0, type=str)
	print(txt)
	res = ner.get_ner(txt, pos=False,tag=True)

	return jsonify(result=res)

@app.route('/api/pos_tag', methods=["GET"])
def pos_tag_api():
	sent = request.args.get('sent', 0, type=str)
	txt=""
	for i in sent.split('<br>'):
		txt+=" ".join("%s/%s" % tup for tup in pos_tag(word_tokenize(i)))+"<br>"
	return jsonify(result=txt)

@app.route('/api/soundex', methods=["GET"])
def soundex_api():
	sent = request.args.get('sent', 0, type=str)
	txt=""
	for i in sent.split('<br>'):
		txt += "<b>Word : </b>"+i+"<br><p>กฎการเข้ารหัสซาวน์เด็กซ์ของ วิชิตหล่อจีระชุณห์กุล และ เจริญ คุวินทร์พันธุ์ - LK82 : "+ lk82(i) +"<br>กฎการเข้ารหัสซาวน์เด็กซ์ของ วรรณี อุดมพาณิชย์ - Udom83 : "+ udom83(i)+"</p><br>"
	return jsonify(result=txt)

@app.errorhandler(500)
def server_error(e):
	logging.exception('An error occurred during a request.')
	return """
	An internal error occurred: <pre>{}</pre>
	See logs for full stacktrace.
	""".format(e), 500

@app.errorhandler(404)
def not_found(e):
	return "404 NOT FOUND"

@app.context_processor
def inject_stuff():
    return dict(
		pythainlp_version=pythainlp.__version__,
		now=datetime.now(),
		app_config=app_config
	)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=port, debug=True)