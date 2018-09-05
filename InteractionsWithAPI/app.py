
from flask import Flask, redirect, url_for, render_template, flash
from forms import PaymentForm

app = Flask(__name__)
app.secret_key = "SecretKey01"
shop_id = 5
payway = "payeer_rub"


@app.route('/')
def index():
    return "GOOD"


@app.route('/login')
def login():

    form = PaymentForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.payment_amount.data, form.payment_currency.data
        ))
        return redirect(url_for('index'))
    return render_template('login.html', title='Payments', form=form)


if __name__ == '__main__':
    app.run()
