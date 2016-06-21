from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
app = Flask(__name__)
app.config.from_object(__name__)

@app.route("/", methods=['GET'])
def loginScreen():
    return render_template('login.html')

@app.route("/login", methods=['POST'])
def login():
	if request.method == 'POST':
		return request.form['user']

if __name__ == "__main__":
    app.run()