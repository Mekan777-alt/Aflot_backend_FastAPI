import os
from dotenv import load_dotenv
import requests
from fastapi import HTTPException

load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
url = os.getenv('URL')


def login_to_bank():
    try:
        response = requests.post(url, data={'client_id': client_id,
                                            'client_secret': client_secret,
                                            'grant_type': 'client_credentials'})

        if response.status_code == 200:

            return response.json()

    except HTTPException as e:

        return e
