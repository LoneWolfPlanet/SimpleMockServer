from urllib.parse import urljoin

# Third-party imports...
import requests

# Local imports...
from constants import BASE_URL

TODOS_URL = urljoin(BASE_URL, 'todos')
USERS_URL = urljoin(BASE_URL, 'users')


def get_todos():
    response = requests.get(TODOS_URL)
    if response.ok:
        return response
    else:
        return None

def get_users():
    response = requests.get(USERS_URL)
    if response.ok:
        return response
    else:
        return None