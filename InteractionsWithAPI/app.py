import json
import hashlib
import logging
import datetime
import requests

from create_db import Payments
from forms import PaymentForm
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import Flask, redirect, url_for, render_template, flash, request, session


app = Flask(__name__)
app.secret_key = "SecretKey01"
shop_id = 5
shop_order_id = 123456
payway = "payeer_rub"

logger = logging.getLogger('Loger')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('info.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


@app.route('/')
def index():
    return "GOOD"


@app.route('/payments', methods=["POST", "GET"])
def payments():

    form = PaymentForm()
    if form.validate_on_submit():

        currency = form.payment_currency.data

        currencies = {'USD': 'usd_api', 'EUR': 'eur_api', 'RUB': 'rub_api'}
        print(request.form['payment_currency'], request.form['description'], '!!!')
        values = [request.form['payment_amount'],
                  request.form['payment_currency'],
                  request.form['description']]
        session['values'] = values
        return redirect(url_for('{}'.format(currencies[currency])))

    return render_template('payments.html', title='Payments', form=form)


def add_to_DB(*args):
    engine = create_engine('sqlite:///payments.db', echo=True)
    # create a Session
    Session = sessionmaker(bind=engine)
    session = Session()

    payment = Payments(args[0], args[1], args[2], args[3])
    session.add(payment)

    # commit the record database
    session.commit()


def create_sign(*args):
    print(args)
    str_for_hash = ":".join(str(arg) for arg in args)
    str_for_hash += app.secret_key
    print(str_for_hash)
    hashh = hashlib.sha256(str.encode(str_for_hash)).hexdigest()
    return hashh


@app.route('/eur_api', methods=['POST', 'GET'])
def eur_api():
    titles = ['amount', 'currency', 'description']
    dictt = {}
    for val, x in zip(titles, session.pop("values", [])):
        dictt[val] = x

    sign = create_sign(':'.join(str(x) for x in [dictt['amount'], dictt['currency'], shop_id, shop_order_id]))
    print(sign)
    add_to_DB(float(dictt['amount']), dictt['currency'], dictt['description'], datetime.datetime.now())
    logger.info('Create EUR pay with values:'+', '.join([dictt['amount'], dictt['currency'], dictt['description']]))
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


@app.route('/test_db')
def test_db():
    engine = create_engine('sqlite:///payments.db', echo=True)
    # create a Session
    Session = sessionmaker(bind=engine)
    session = Session()

    payments = session.query(Payments).all()
    return ','.join(payment.description for payment in payments)


if __name__ == '__main__':
    app.run()
