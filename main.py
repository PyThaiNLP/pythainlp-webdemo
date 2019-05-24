# -*- coding: utf-8 -*-
"""
PyThaiNLP Demo Online
V 0.1
พัฒนาโดย นาย วรรณพงษ์  ภัททิยไพบูลย์
"""
import logging
import json
import os

from flask import Flask, render_template, abort, request,jsonify
from datetime import datetime

import pythainlp
from pythainlp.tokenize import word_tokenize
from pythainlp.tokenize import tcc
from pythainlp.tag import pos_tag
from pythainlp.soundex import lk82, udom83

port = os.environ['PORT'] if os.environ['PORT'] else 80

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

@app.route('/api/word_tokenizer', methods=["GET"])
def word_tokenizer_api():

	sent = request.args.get('sent', 0, type=str)
	engine = request.args.get('engine', 0, type=str)

	tokenised = word_tokenize(sent, engine=engine)
	
	return jsonify(result='|'.join(tokenised))

@app.route('/api/tcc', methods=["GET"])
def tcc_api():
	sent = request.args.get('sent', 0, type=str)
	txt=""
	for i in sent.split('<br>'):
		txt+=tcc.tcc(i)+"<br>"
	return jsonify(result=txt)

@app.route('/api/pos_tag', methods=["GET"])
def pos_tag_api():
	sent = request.args.get('sent', 0, type=str)
	txt=""
	for i in sent.split('<br>'):
		txt+=" ".join("%s/%s" % tup for tup in pos_tag(word_tokenize(i),engine='artagger'))+"<br>"
	return jsonify(result=txt)

@app.route('/api/soundex', methods=["GET"])
def soundex_api():
	sent = request.args.get('sent', 0, type=str)
	txt=""
	for i in sent.split('<br>'):
		txt+="<b>Word : </b>"+i+"<br><p>กฎการเข้ารหัสซาวน์เด็กซ์ของ วิชิตหล่อจีระชุณห์กุล และ เจริญ คุวินทร์พันธุ์ - LK82 : "+LK82(i)+"<br>กฎการเข้ารหัสซาวน์เด็กซ์ของ วรรณี อุดมพาณิชย์ - Udom83 : "+Udom83(i)+"</p><br>"
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
		sample_text="คนที่ฝึกภาษาอังกฤษ แม้ว่าต่างคนจะต่างความต้องการ  แต่อย่างหนึ่งที่ดูจะเหมือนกัน คือ อยากอ่านข่าวภาษาอังกฤษได้คล่องเหมือนอ่านข่าวภาษาไทย  ผมสรุปอย่างนี้เพราะมี 2 บทความในเว็บนี้ที่ท่านผู้อ่านเข้าไปอ่านมากทีเดียว"
	)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=port, debug=True)