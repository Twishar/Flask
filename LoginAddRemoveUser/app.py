from flask import Flask, request, Response, render_template, flash, session, redirect, url_for

from create_db import Users
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import logging
logging.basicConfig(filename='logging.log', level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and request.form.get('check') == 'Login':

        user_name, password = request.form['username'], request.form['password']
        engine = create_engine('sqlite:///users.db', echo=True)
        # create a Session
        Session = sessionmaker(bind=engine)
        session = Session()
        notes = {}
        user = session.query(Users).filter(Users.name == user_name, Users.password == password).all()

        if user == []:
            flash("Sorry, Bro. Firstly registration")
            logging.warning("Not registered user: {}".format(user_name))
            return redirect(url_for('login'))

        return redirect(url_for('users_info', user_name=user_name))

    if request.method == 'POST' and request.form.get('check') == 'Registration':

        engine = create_engine('sqlite:///users.db', echo=True)
        # create a Session
        Session = sessionmaker(bind=engine)
        session = Session()
        check = session.query(Users).filter(Users.name == request.form['username']).all()

        if check != []:
            flash("Sorry, Bro. This name is occupied")
            logging.warning("Name:{} is occupied".format(request.form['username']))
            return redirect(url_for('login'))
        user = Users(request.form['username'], request.form['password'], '')
        session.add(user)
        session.commit()

        flash("Cool, lets try to login!")
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/users_info', methods=['GET', 'POST'])
def users_info():
    if request.method == 'POST':

        user_name = request.args.get('user_name')

        engine = create_engine('sqlite:///users.db', echo=True)
        # create a Session
        Session = sessionmaker(bind=engine)
        session = Session()

        check = session.query(Users).filter(Users.name == request.form['username']).all()
        if check != []:
            flash("Sorry, Bro. This name is occupied")
            logging.warning("Name:{} is occupied".format(request.form['username']))
            return redirect(url_for('users_info', user_name=user_name))

        user = Users(request.form['username'], request.form['password'], user_name)
        session.add(user)

        # commit the record database
        session.commit()

    user_name = request.args.get('user_name')
    engine = create_engine('sqlite:///users.db', echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    if user_name != "admin":
        child_users = session.query(Users).filter(Users.parent_name == user_name).all()
    else:
        child_users = session.query(Users).filter(Users.name != user_name).all()
    childs = []
    for child in child_users:
        childs.append(child.name)
    return render_template('users_info.html', user_name=user_name, childs=childs)


@app.route('/remove_user', methods=['GET', 'POST'])
def remove_user():
    if request.method == 'POST':
        engine = create_engine('sqlite:///users.db', echo=True)
        Session = sessionmaker(bind=engine)
        session = Session()
        user = session.query(Users).filter_by(name=request.form['remove']).first()
        if user != []:
            session.delete(user)
            session.commit()

    return redirect(url_for("users_info", user_name=request.form['parent_name']))


@app.route('/log_out')
def log_out():
    return redirect('/login')


if __name__ == '__main__':
    app.run()
