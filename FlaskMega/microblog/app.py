
from flask import Flask, render_template
from config import Config
from forms import LoginForm

app = Flask(__name__)
app.config.from_object(Config)


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


@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign in', form=form)


if __name__ == '__main__':
    app.run()
