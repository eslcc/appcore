from flask import Blueprint, request
import json
from adfslogin import adfslogin, AdfsLoginFailed
import traceback

neutron = Blueprint('neutron', __name__)


@neutron.route('/login', methods=['POST'])
def login():
    email = request.values['email']
    password = request.values['password']

    try:
        result = adfslogin(email, password)
        return json.dumps({
            'error': False,
            'cookie': result
        })
    except AdfsLoginFailed as e:
        return json.dumps({
            'error': True,
            'exception': traceback.format_exc()
        })