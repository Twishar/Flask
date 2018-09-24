
from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'example@gmail.com'
app.config['MAIL_PASSWORD'] = 'pass'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True


mail = Mail(app)


@app.route('/')
def index():

    return render_template('index.html')


@app.route('/guest', methods=['POST', 'GET'])
def guest():

    name = request.form.get('name')
    email = request.form.get('email')
    link = request.form.get('link')
    description = request.form.get('description')
    msg = Message('Info from Guest form', sender='example@gmail.com',
                  recipients=['cctncct@gmail.com'])
    msg.body = "User name: {}\n" \
               "User email: {}\n" \
               "Guest link: {}\n" \
               "Why he?: {}\n".format(name, email,
                                      link, description)
    with app.app_context():
        mail.send(msg)
    return redirect(url_for('index'))


app.run()
