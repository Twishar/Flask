
from flask import Flask, render_template, request


app = Flask(__name__)


@app.route('/')
def index():

    return render_template('index.html')


@app.route('/guest', methods=['POST', 'GET'])
def guest():

    name = request.form.get('name')
    print(name)
    return '<h1>ASFASF</h1>'


app.run()
