import json

from create_db import Payments
from forms import PaymentForm
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import Flask, redirect, url_for, render_template, flash, request, session
import requests


app = Flask(__name__)
app.secret_key = "SecretKey01"
shop_id = 5
payway = "payeer_rub"


@app.route('/')
def index():
    return "GOOD"


@app.route('/payments', methods=["POST", "GET"])
def payments():

    form = PaymentForm()
    if form.validate_on_submit():

        currency = form.payment_currency.data

        currencies = {'USD': 'usd_api', 'EUR': 'eur_api', 'RUB': 'rub_api'}

        """
        engine = create_engine('sqlite:///payments.db', echo=True)
        # create a Session
        Session = sessionmaker(bind=engine)
        session = Session()

        payment = Payments(request.form['payment_amount'], request.form['payment_currency'], request.form['description'])
        session.add(payment)

        # commit the record database
        session.commit()
        """
        print(request.form['payment_currency'], request.form['description'], '!!!')
        values = [request.form['payment_amount'],
                  request.form['payment_currency'],
                  request.form['description']]
        session['values'] = values
        return redirect(url_for('{}'.format(currencies[currency])))

    return render_template('payments.html', title='Payments', form=form)


@app.route('/usd_api')
def usd_api():
    values  = []
    for k in session.pop('values', []):
        values.append(k)
    print(values)

    return ''


@app.route('/eur_api')
def eur_api():
    return ''


@app.route('/rub_api')
def rub_api():
    return ''


@app.route('/test', methods=['GET', 'POST'])
def test_for_usd():

    data = {"payer_currency": 643,
            "shop_amount": "23.15",
            "shop_currency": 643,
            "shop_id": "5",
            "shop_order_id": 123456,
            "sign": "091ee6f0bce195a508231ee0d62d7645bd0b38b63e22bde78046b277d6988045"
            }

    r = requests.post('https://core.piastrix.com/bill/create', data=json.dumps(data), headers={'Content-Type': 'application/json'})
    print(r.headers['content-type'])
    print(r.json())
    return 'ff'


if __name__ == '__main__':
    app.run()
