import requests
from bs4 import BeautifulSoup


class AdfsLoginFailed(Exception):
    pass


def adfslogin(email, password):
    s = requests.Session()

    # First, request SMS to be redirected to ADFS
    r = s.get('https://sms.eursc.eu/sso.php')

    # Second, log in to ADFS
    # Find the URL to continue the flow
    soup = BeautifulSoup(r.text, "html.parser")
    form = soup.select('#loginForm')
    form_url = 'https://sts.eursc.eu' + form[0]['action']

    payload = {'AuthMethod': 'FormsAuthentication', 'UserName': email, 'Password': password}

    r2 = s.post(form_url, data=payload)

    # Third, follow ADFS's form to be redirected back to SMS
    soup2 = BeautifulSoup(r2.text, "html.parser")
    form2 = soup2.select('form')
    form_url2 = form2[0]['action']

    # ADFS's intermediary form has a bunch of inputs we need to finish the SAML flow
    payload2 = {}

    try:
        for input in soup2.select('input[type=\'hidden\']'):
            payload2[input['name']] = input['value']

        r3 = s.post(form_url2, data=payload2)

        # Epic success!
        return s.cookies['PHPSESSID']
    except KeyError as e:
        raise AdfsLoginFailed(e)
