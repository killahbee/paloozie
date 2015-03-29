from flask import Flask, g, render_template, request, redirect, session, jsonify, json, escape, url_for, send_file
from flask_wtf.csrf import CsrfProtect
import db

import re
import fins
import uuid
import psycopg2

app = Flask(__name__)

@app.teardown_request
def teardown_request(exception):
	db = getattr(g, 'db', None)

	if db is not None:
		db.close()

@app.route('/')
def home():

	return render_template('home.html')

@app.route('/paloozies/', methods=["GET", "POST"])
@app.route('/paloozies/<paloozie_id>/', methods=["GET", "POST"])
def paloozies( paloozie_id = None ):

	if request.method == "GET":

		if paloozie_id == None:
			# show create a paloozie page
			return render_template('create_paloozie.html')

		else:

			try:
				sql_query = "SELECT * FROM paloozie_urls, paloozies WHERE paloozie_urls.url = %s AND paloozie_urls.id = paloozies.id;"
				sql_data = (paloozie_url, )

				cur = conn.cursor()
				cur.execute( sql_query, sql_data )
				paloozie = cur.fetchone()
				cur.close()

				paloozie = { "name": paloozie[0], "description": paloozie[1], "location_name": paloozie[2], "isadmin": paloozie[3] }

			except Exception, e:
				print e
				paloozie = {}

			# show a paloozie
			return render_template('view_paloozie.html')

	elif request.method == "POST":
		
		if paloozie_id == None:
			# create a new paloozie
			print request.form

			try:
				sql_query = """BEGIN;
				    WITH paloozie_insert AS (
				        INSERT INTO paloozies ( name ) VALUES ( 'foo' ) RETURNING id
				    ),
				    paloozie_url AS (
				        INSERT INTO paloozie_urls ( pid ) VALUES ( (SELECT id FROM paloozie_insert) ) RETURNING pid
				    )
				    INSERT INTO paloozie_urls ( pid, isadmin ) VALUES ( (SELECT pid FROM paloozie_url), TRUE ) RETURNING pid;
				COMMIT;"""

				sql_data = (paloozie_url, )

				cur = conn.cursor()
				cur.execute( sql_query, sql_data )
				paloozie_id = cur.fetchone()[0]
				cur.close()

				paloozie = { "id": paloozie_id }

			except db.psycopg2.DatabaseError, e:
				print e
				paloozie = {}

		else:
			# edit a paloozie
			pass

@app.route('/create/paloozie/', methods=["GET"])
def create_paloozie():

	return redirect(url_for("paloozies"))

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