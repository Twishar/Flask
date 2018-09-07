import json
import hashlib
import logging
import datetime
import requests

from config import *
from create_db import Payments
from forms import PaymentForm
from sqlalchemy import create_engine
from flask_bootstrap import Bootstrap
from sqlalchemy.orm import sessionmaker
from flask import Flask, redirect, url_for, render_template, flash, request, session
from flask_sslify import SSLify

app = Flask(__name__)
app.secret_key = secret_key

bootstrap = Bootstrap(app)
SSLify(app)

logger = logging.getLogger('Loger')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('info.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


@app.route('/', methods=["POST", "GET"])
def payments():

    form = PaymentForm()
    if form.validate_on_submit():

        currency = form.payment_currency.data
        currencies = {'USD': 'usd_api', 'EUR': 'eur_api', 'RUB': 'rub_api'}

        values = [request.form['payment_amount'],
                  currency_code[request.form['payment_currency']],
                  request.form['description']]

        session['values'] = values
        return redirect(url_for('{}'.format(currencies[currency])))

    return render_template('payments.html', form=form)


@app.route('/eur_api', methods=['POST', 'GET'])
def eur_api():

    data_from_form = get_data_from_session(session)

    sign = create_sign(':'.join(str(x) for x in [data_from_form['amount'], data_from_form['currency'],
                                                 shop_id, shop_order_id]))

    add_to_db(float(data_from_form['amount']), data_from_form['currency'],
              data_from_form['description'], datetime.datetime.now())

    logger.info('Create EUR pay with amount: {} and description: {}'.format(data_from_form['amount'],
                                                                            data_from_form['description']))

    data_from_form['sign'] = sign
    data_from_form['shop_id'] = shop_id
    data_from_form['shop_order_id'] = shop_order_id
    return render_template('api_for_eur.html', dictt=data_from_form)


@app.route('/rub_api')
def rub_api():

    data_from_form = get_data_from_session(session)

    data_for_request = {
            "amount": data_from_form['amount'],
            "currency": data_from_form['currency'],
            "payway": payway,
            "shop_id": shop_id,
            "shop_order_id": shop_order_id,
            "sign": create_sign(data_from_form['amount'], data_from_form['currency'], payway, shop_id, shop_order_id)
            }

    r = requests.post('https://core.piastrix.com/invoice/create', data=json.dumps(data_for_request),
                      headers={'Content-Type': 'application/json'})

    data_for_api = r.json()
    if data_for_api["message"] == 'Ok':
        add_to_db(float(data_from_form['amount']), data_from_form['currency'],
                  data_from_form['description'], datetime.datetime.now())

        logger.info('Create RUB pay with amount: {} and description: {}'.format(data_from_form['amount'],
                                                                                data_from_form['description']))

        return render_template('api_for_rub.html', data=data_for_api['data']['data'],
                               url=data_for_api['data']['url'], method=data_for_api['data']['method'])
    else:
        flash(data_for_api["message"])
        return redirect(url_for('payments'))


@app.route('/usd_api', methods=['POST', 'GET'])
def usd_api():

    data_from_form = get_data_from_session(session)

    data_for_request = {
            "payer_currency": data_from_form['currency'],
            "shop_amount": data_from_form['amount'],
            "shop_currency": data_from_form['currency'],
            "shop_id": shop_id,
            "shop_order_id": shop_order_id,
            "sign": create_sign(data_from_form['currency'], data_from_form['amount'],
                                data_from_form['currency'], shop_id, shop_order_id)
            }

    r = requests.post('https://core.piastrix.com/bill/create', data=json.dumps(data_for_request),
                      headers={'Content-Type': 'application/json'})

    data_for_api = r.json()

    if data_for_api["message"] == 'Ok':
        add_to_db(float(data_from_form['amount']), data_from_form['currency'],
                  data_from_form['description'], datetime.datetime.now())

        logger.info('Create USD pay with amount: {} and description: {}'.format(data_from_form['amount'],
                                                                                data_from_form['description']))

        link = data_for_api['data']['url']
        return redirect(link)
    else:
        flash(data_for_api["message"])
        return redirect(url_for('payments'))


def add_to_db(*args):
    engine = create_engine('sqlite:///payments.db', echo=True)
    # create a Session
    Session = sessionmaker(bind=engine)
    session = Session()

    payment = Payments(args[0], args[1], args[2], args[3])
    session.add(payment)

    # commit the record database
    session.commit()


def create_sign(*args):
    str_for_hash = ":".join(str(arg) for arg in args) + app.secret_key
    hashh = hashlib.sha256(str.encode(str_for_hash)).hexdigest()
    return hashh


def get_data_from_session(session_):
    titles = ['amount', 'currency', 'description']
    data_for_api = {}

    for title, value in zip(titles, session_.pop("values", [])):
        data_for_api[title] = value
    return data_for_api


if __name__ == '__main__':
    app.run()
