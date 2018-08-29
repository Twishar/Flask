
from config import Config
from forms import LoginForm
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, flash, redirect, url_for

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Jojo'}
    posts = [
        {
            'author': {'username': 'Jojo'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool'
        },
        {
            'author': {'username': 'SHake'},
            'body': 'Hey Man'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data
        ))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign in', form=form)


if __name__ == '__main__':
    app.run()
