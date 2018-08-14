from flask import Flask, request, Response, render_template, flash, session, redirect, url_for

from create_db import Users
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/')
def root_response():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and request.form.get('check') == 'Login':

        user_name = request.form['username']
        print(user_name)
        engine = create_engine('sqlite:///users.db', echo=True)
        # create a Session
        Session = sessionmaker(bind=engine)
        session = Session()
        notes = {}
        user = session.query(Users).filter(Users.name == user_name).all()
        print(user)
        print(user == [])

        if user == []:
            print('check')
            flash("Sorry, Bro. Firstly registration")
            return redirect(url_for('login'))

        return redirect(url_for('new', user_name=user_name))

    if request.method == 'POST' and request.form.get('check') == 'Registration':

        engine = create_engine('sqlite:///users.db', echo=True)
        # create a Session
        Session = sessionmaker(bind=engine)
        session = Session()

        user = Users(request.form['username'], request.form['password'], '')
        session.add(user)
        session.commit()

        flash("Cool, lets try to login!")
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':

        user_name = request.args.get('user_name')

        engine = create_engine('sqlite:///users.db', echo=True)
        # create a Session
        Session = sessionmaker(bind=engine)
        session = Session()

        user = Users(request.form['username'], request.form['password'], user_name)
        session.add(user)

        # commit the record database
        session.commit()

        result = request.form
        print(result['username'])
        return render_template('test.html', result=result)

    user_name = request.args.get('user_name')
    return render_template('new.html', user_name=user_name)


@app.route('/test_val', methods=['GET', 'POST'])
def test_val():

    engine = create_engine('sqlite:///users.db', echo=True)
    # create a Session
    Session = sessionmaker(bind=engine)
    session = Session()
    notes = {}
    for user in session.query(Users).filter(Users.parent_name == 'admin'):
        notes[user.name] = [user.parent_name, user.password]

    print(notes)

    return ''


if __name__ == '__main__':
    app.run()
