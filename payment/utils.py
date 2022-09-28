import hashlib
from collections import OrderedDict

from bs4 import BeautifulSoup


def get_url_from_content(html: str):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find('pg_redirect_url').text


def get_url_from_content_result(html: str, teg: str):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find(teg).text


def generate_sig(data: dict, method: str):
    data = OrderedDict(sorted(data.items()))
    string = method

    for key, value in data.items():
        if value and key != 'pg_sig':
            string += ";{}".format(value)

    string += ";{}".format("LeFnP16MP6AU6YKc")
    pg_sig = hashlib.md5(string.encode()).hexdigest()
    data['pg_sig'] = pg_sig
    return data