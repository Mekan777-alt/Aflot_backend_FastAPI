import os
import requests
from dotenv import load_dotenv

load_dotenv()


def get_token():
    url = os.getenv('URL_KASSA')

    header = {
        'Content-Type': 'application/json',
    }

    body = {
        "login": os.getenv('LOGIN_KASSA'),
        "pass": os.getenv('PASSWORD_KASSA'),
    }

    res = requests.post(url, headers=header, json=body)

    if res.status_code == 200:

        return res.json()

    return None

