import requests
from config import constants
from utils import parseutils
from utils import commonutils

URL = constants.BASE_URL


def get_response(url,param_dict):
    response = requests.get(url,params=param_dict)
    if response.status_code == 200:
        return response.json()
    else:
        return "error"
