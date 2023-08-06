import json
import re
import os
from threading import Thread
from celery import Celery
from functools import wraps
from flask_jwt_extended import get_jwt_identity
from itsdangerous import URLSafeTimedSerializer
from flask import url_for
from flask_mail import Mail, Message


class Validators:
    """Class with validation methods."""

    def __init__(self, variable=None):
        self.variable = variable

    def email(self):
        """Check if the format of the email is valid."""
        if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+[a-zA-Z0-9-.]+$)",
                    self.variable):
            return True
        return False

    def password(self):
        """Check if that the password is eight long character string with atleast one lowercase character, one uppercase character, one number, and one special character."""
        if re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", self.variable):
            return True
        return False

    def phone(self):
        """Check if that the phone number satisfies kenyan format."""
        if re.match(r"^(?:254|\+254|0)?(7(?:(?:[129][0-9])|(?:0[0-8])|(4[0-1]))[0-9]{6})$", self.variable):
            return True
        return False

    def safaricom(self):
        """Check if that the phone number satisfies safaricom format."""
        if re.match(r"^(?:254|\+254|0)?(7(?:(?:[129][0–9])|(?:0[0–8])|(4[0–1]))[0–9]{6})$", self.variable):
            return True
        return False

    def airtel(self):
        """Check if that the phone number satisfies airtel format."""
        if re.match(r"^(?:254|\+254|0)?(7(?:(?:[3][0-9])|(?:5[0-6])|(8[0-9]))[0-9]{6})$", self.variable):
            return True
        return False

    def orange(self):
        """Check if that the phone number satisfies orange format."""
        if re.match(r"^(?:254|\+254|0)?(77[0-6][0-9]{6})$", self.variable):
            return True
        return False

    def equitel(self):
        """Check if that the phone number satisfies equitel format."""
        if re.match(r"^(?:254|\+254|0)?(76[34][0-9]{6})$", self.variable):
            return True
        return False

    def integer(self):
        """Check if the input is an integer."""
        if re.match(r"^[-+]?([1-9]\d*|0)$", self.variable):
            return True
        return False

    def name(self):
        """Check if the input is a word."""
        if re.match(r"^[A-Za-z]{2,25}||\s[A-Za-z]{2,25}$", self.variable):
            return True
        return False

    def error_in_json_keys(self, request):
        """Display errors if json keys don't match."""
        res_keys = self.variable
        errors = []
        for key in res_keys:
            if key not in request.json:
                errors.append(key)
        return errors

    def input_restriction(self, input_data):
        """Verify that the user input is what is expected."""
        form = input_data
        if self.variable not in form:
            return False
        return True


class Serializer:
    """This class serializes data."""

    @classmethod
    def serialize(cls, response, status_code, message=200):
        """Serializes data output."""
        if status_code in (400, 401, 403, 404, 405, 500):
            return json.dumps({
                "status": status_code,
                "message": message,
                "error": response
            }), status_code
        return json.dumps({
            "status": status_code,
            "message": message,
            "data": response
        }), status_code

    @classmethod
    def raise_error(cls, status, msg):
        """Display error message."""
        return json.dumps({
            "status": status,
            "message": msg
        }), status

    @classmethod
    def on_success(cls, status, msg):
        """Display successful message."""
        return json.dumps({
            "status": status,
            "message": msg
        }), status

    @classmethod
    def page_not_found(cls, e):
        """Capture not found error."""
        return json.dumps({
            "status": "404",
            "message": "resource not found"
        }), 404

    @classmethod
    def method_not_allowed(cls, e):
        """Capture method not allowed error."""
        return json.dumps({
            "status": "405",
            "message": "method not allowed"
        }), 405

    @classmethod
    def internal_server_error(cls, e):
        """Capture internal server error."""
        return json.dumps({
            "status": "500",
            "message": "internal server error"
        }), 500

    @classmethod
    def default_encode_token(cls, SECRET_KEY, variable, salt='default-key'):
        """Encode token using unique variable."""
        serializer = URLSafeTimedSerializer(SECRET_KEY)
        return serializer.dumps(variable, salt=salt)

    @classmethod
    def default_decode_token(cls, SECRET_KEY, token, salt='default-key', expiration=3600):
        """Decode token and get the variable."""
        serializer = URLSafeTimedSerializer(SECRET_KEY)
        try:
            variable = serializer.loads(
                token, salt=salt, max_age=expiration)
            return variable
        except Exception:
            return False

    @classmethod
    def generate_url(cls, endpoint, token):
        """Generate url to concatenate at the end of another url."""
        return url_for(endpoint, token=token, _external=True)


def admin_required(func, users):

    @ wraps(func)
    def wrapper_function(*args, **kwargs):

        try:
            cur_user = [
                user for user in users if user['email'] == get_jwt_identity()]
            user_role = cur_user[0]['role']
            if user_role != 'admin':
                return {
                    'message': 'This activity can only be completed by the admin'}, 403  # Forbidden
            return func(*args, **kwargs)
        except Exception as e:
            return {"message": e}

    return wrapper_function


def send_async_email(app, msg):
    """Send asychronous email."""
    mail = Mail()
    with app.app_context():
        try:
            mail.send(msg)
        except ConnectionRefusedError:
            return json.dumps({
                "status": "500",
                "msg": "Mail server not working"
            }), 500


def send_email(app, subject, sender, recipients, text_body, html_body):
    """Message body."""
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()


def make_celery(app, broker_url, backend_url):
    celery = Celery(
        app.import_name,
        broker=broker_url,
        backend=backend_url
    )
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
