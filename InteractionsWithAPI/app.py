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


@app.route('/eur_api', methods=['POST', 'GET'])
def eur_api():

    return render_template('eur_test_templ.html')


@app.route('/rub_api')
def rub_api():
    data = {
            "amount": "12.34",
            "currency": "643",
            "payway": "payeer_rub",
            "shop_id": "5",
            "shop_order_id": "123456",
            "sign": "b2ab7f0ae2788055305cf7f53a0a0904179b3a05b14fd945bf7da06bbaafc67a"
            }

    r = requests.post('https://core.piastrix.com/invoice/create', data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    print(r.headers['content-type'])
    print(r.json())
    data = r.json()

    link = data['data']['data']['referer']
    return redirect(link)


@app.route('/usd_api', methods=['POST', 'GET'])
def usd_api():

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
    data = r.json()
    link = data['data']['url']
    return redirect(link)


if __name__ == '__main__':
    app.run()
