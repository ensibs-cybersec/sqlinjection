from flask import Flask
from flask import make_response
from flask import request
from flask import render_template

import requests, json
import MySQLdb

app = Flask(__name__)

@app.route('/', methods=['GET'])
def racine():

    return render_template('index.html')

@app.route('/init', methods=['POST'])
def init():

    try:
        conn = MySQLdb.connect (host = "mysql", user = "root", passwd = "Ensibs56")
        cursor = conn.cursor()
        cursor.execute('DROP DATABASE IF EXISTS test')
        cursor.execute('CREATE DATABASE test')
        cursor.execute('USE test')
        cursor.execute('CREATE TABLE individuals (lastname varchar(50), firstname varchar(50))')
        cursor.execute("INSERT INTO individuals VALUES ('Lagaffe', 'Gaston')")
        cursor.execute("INSERT INTO individuals VALUES ('Gouigoux', 'Jean-Philippe')")
        conn.commit();
        conn.close();

    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])

    return "Database 'test' initialized with dummy individuals"

@app.route('/data', methods=['GET'])
def data():

    try:
        conn = MySQLdb.connect (host = "mysql", user = "root", passwd = "Ensibs56", db = "test")
        cursor = conn.cursor()
        
        name = request.args['restriction']
	if request.args.has_key('securemode') and request.args['securemode'] == 'on':
            cursor.execute("SELECT * FROM individuals WHERE lastname = %s", (name,))
	else:
	    cursor.execute("SELECT * FROM individuals WHERE lastname = '%s'" % name)

        if cursor.rowcount > 0:
            return render_template('results.html', cursor=cursor)
        else:
            return "no item found"
            
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])

if __name__ == '__main__':
    app.run(host='0.0.0.0')
