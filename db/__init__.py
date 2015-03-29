import psycopg2, re
import psycopg2.extras
from flask import g

def connect_db():
	return psycopg2.connect(database="mybox", user="mybox_admin", password="qazwsx", host="localhost")

def get_db():
	db = getattr(g, 'db', None)

	if db is None:
		db = g.db = connect_db()

	return db