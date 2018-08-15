import logging

from create_db import Users
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, request, render_template, flash, redirect, url_for
from flask_sslify import SSLify


logging.basicConfig(filename='logging.log', level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
# sslify = SSLify(app)


@app.route('/')
def index():
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and request.form.get('username') == '' and request.form.get('password') == '':
        flash("Type u username and password")
        logging.warning("Blank fields in login")
        return redirect(url_for('login'))

    if request.method == 'POST' and request.form.get('check') == 'Login':

        user_name, password = request.form['username'], request.form['password']
        engine = create_engine('sqlite:///users.db', echo=True)
        # create a Session
        Session = sessionmaker(bind=engine)
        session = Session()
        user = session.query(Users).filter_by(name=user_name).first()

        if user == []:
            flash("Sorry, my dear friend. Firstly registration")
            logging.warning("Not registered user: {}".format(user_name))
            return redirect(url_for('login'))

        elif not check_password_hash(user.hash, password):
            flash("Sorry, my dear friend. Wrong password")
            logging.warning("Wrong password: {}".format(user_name))
            return redirect(url_for('login'))

        return redirect(url_for('users_info', user_name=user_name))

    if request.method == 'POST' and request.form.get('check') == 'Registration':

        if request.form['username'] == '' or request.form['password'] == '':
            flash("Type not null username or password please")
            redirect(url_for('login'))

        engine = create_engine('sqlite:///users.db', echo=True)
        # create a Session
        Session = sessionmaker(bind=engine)
        session = Session()
        check = session.query(Users).filter(Users.name == request.form['username']).all()

        if check != []:
            flash("Sorry, my dear friend. This name is occupied")
            logging.warning("Name:{} is occupied".format(request.form['username']))
            return redirect(url_for('login'))

        pass_hash = generate_password_hash(request.form['password'])
        user = Users(request.form['username'], request.form['password'], '', pass_hash)
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
            flash("Sorry, my dear friend. This name is occupied")
            logging.warning("Name:{} is occupied".format(request.form['username']))
            return redirect(url_for('users_info', user_name=user_name))

        pass_hash = generate_password_hash(request.form['password'])
        user = Users(request.form['username'], request.form['password'], user_name, pass_hash)
        session.add(user)

        # commit the record database
        session.commit()

    user_name = request.args.get('user_name')
    engine = create_engine('sqlite:///users.db', echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()

    if user_name != "admin":
        child_users = session.query(Users).filter(Users.parent_name == user_name).all()
        childs = []

        for child in child_users:
            childs.append(child.name)

        return render_template('users_info.html', user_name=user_name, childs=childs)

    else:
        users = session.query(Users.parent_name).distinct().all()
        parents_childs = {}

        for p_user in users:
            parents_childs[p_user[0]] = [child.name for child in
                                         session.query(Users).filter(Users.parent_name == p_user[0]).all()]

        logging.info(parents_childs)
        return render_template('users_info.html', user_name=user_name, childs=parents_childs, admin=True)


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
