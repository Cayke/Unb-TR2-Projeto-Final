from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
import getServerRequests
import json 

app = Flask(__name__)
app.config.from_object(__name__)

@app.route("/", methods=['GET'])
def loginScreen():
    return render_template('login.html')

@app.route("/login", methods=['POST'])
def login():
	if request.method == 'POST':
		return redirect(url_for('filesTree'))

@app.route("/filesTree", methods=['GET','POST'])
def filesTree():
	with open('templates/test.json') as data_file: 
		jsonFile = json.load(data_file)
	return render_template('tree.html',json=jsonFile)

if __name__ == "__main__":
    app.run()