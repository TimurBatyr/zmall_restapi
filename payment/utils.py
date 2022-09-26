import hashlib
from collections import OrderedDict

from bs4 import BeautifulSoup
from decouple import config


def generate_sig(data: dict, method: str) -> dict:
    id=data['id']
    amont=data['amount']
    des=data['description']
    salt=data['salt']

    data = dict(
        pg_order_id=id,
        pg_merchant_id=535456,
        pg_amount=int(amont[0]),
        pg_description=des[0],
        pg_salt=salt[0],
        pg_success_url = 'http://127.0.0.1:8000/api/success',
        pg_failure_url ='http://127.0.0.1:8000/api/failure'
    )

    data = OrderedDict(sorted(data.items()))

    string = method
    for key, value in data.items():

        if value and key != 'pg_sig':
            string += ";{}".format(value)

    string += ";{}".format("LeFnP16MP6AU6YKc")
    pg_sig = hashlib.md5(string.encode()).hexdigest()
    data['pg_sig'] = pg_sig
    return data

def get_url_from_content(html: str):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find('pg_redirect_url').text