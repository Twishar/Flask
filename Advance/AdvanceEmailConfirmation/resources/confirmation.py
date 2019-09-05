from flask import make_response, render_template
from flask_restful import Resource

from models.confirmation import ConfirmationModel
from models.user import UserModel

EXPIRED = "The link has expired."
NOT_FOUND = "Confirmation reference not found."
ALREADY_CONFIRMED = "Registration has already been confirmed."


class Confirmation(Resource):

    @classmethod
    def get(cls, confirmation_id: str):
        """Return confirmation HTML page."""

        confirmation = ConfirmationModel.find_by_id(confirmation_id)

        if not confirmation:
            return {"message": NOT_FOUND}, 404

        if confirmation.expired:
            return {"message": EXPIRED}, 400

        if confirmation.confirmed:
            return {"message": ALREADY_CONFIRMED}, 400

        confirmation.confirmed = True
        confirmation.save_to_db()

        headers = {"Content-Type": "text/html"}
        return make_response(
            render_template("confirmation_page.html", email=confirmation.user.email),
            200,
            headers
        )


class ConfirmationByUser(Resource):

    @classmethod
    def get(cls, user_id: int):
        """Returns confirmations for a given user. Use for testing"""
        pass

    @classmethod
    def post(cls):
        """Resend confirmation email"""
        pass
