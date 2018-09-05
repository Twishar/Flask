
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired


class PaymentForm(FlaskForm):
    payment_amount = FloatField('Amount', validators=[DataRequired()])
    payment_currency = SelectField('Currency',
                                   choices=[('EUR', 'EUR'), ('USD', 'USD'), ('RUB', 'RUB')]
                                   )
    description = TextAreaField('Description')
    submit = SubmitField('Pay')
