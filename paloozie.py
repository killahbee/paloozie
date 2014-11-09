from flask import Flask, render_template, request, redirect, session, jsonify, json, escape, url_for, send_file
from flask_wtf.csrf import CsrfProtect

import re
import fins
import uuid
import psycopg2

conn = psycopg2.connect(database="paloozie", host="localhost")

app = Flask(__name__)

@app.route('/')
def home():

	return render_template('home.html')

@app.route('/create/paloozie/', methods=["GET", "POST"])
def create_paloozie():

	if request.method == "GET":
		return render_template('create_paloozie.html')

	elif request.method == "POST":
		paloozie_id = str(uuid.uuid1())

		print request.form

@app.route('/paloozie/<paloozie_url>/')
def view_paloozie(paloozie_url):

	try:
		sql_query = "SELECT paloozies.name, paloozies.description, paloozies.location_name, paloozie_urls.isadmin FROM paloozie_urls, paloozies WHERE paloozie_urls.url = %s AND paloozie_urls.pid = paloozies.pid;"
		sql_data = (paloozie_url, )

		cur = conn.cursor()
		cur.execute( sql_query, sql_data )
		paloozie = cur.fetchone()
		cur.close()

		paloozie = { "name": paloozie[0], "description": paloozie[1], "location_name": paloozie[2], "isadmin": paloozie[3] }

	except Exception, e:
		print e
		paloozie = {}

	return render_template('view_paloozie.html',
		paloozie = paloozie)

if __name__ == '__main__':
	app.run(debug=True)
	# app.run(host='0.0.0.0')