import requests
from dotenv import load_dotenv
import os

load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')


def get_token_from_bank():
    url = "https://auth.bankingapi.ru/auth/realms/kubernetes/protocol/openid-connect/token"

    req = requests.post(url,
                        {
                            "grant_type": "client_credentials",
                            "client_id": client_id,
                            "client_secret": client_secret
                        })

    if req.status_code != 200:
        return None

    return req.json()


def send_order():

    url = "https://hackaton.bankingapi.ru/api/smb/efcp/e-commerce/api/v1/orders"

    auth = get_token_from_bank()

    headers = {
        "X-IBM-Client-Id": client_id,
        "Authorization": f"Bearer {auth['access_token']}",
        "Content-Type": "application/json"
    }

    data = {
        "orderId": "1",
        "orderName": "Заказ №10000000101",
        "amount": {
            "value": 10.00,
            "code": "RUB"
        }
    }

    request = requests.post(url, headers=headers, data=data)

    return request.json()

