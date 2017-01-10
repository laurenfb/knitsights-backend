from config import *
import requests

URL = 'https://api.ravelry.com/'

class APIWrapper:
    @staticmethod
    def get_current_user_projects(current_username):
        r = requests.get(URL + 'projects/' + current_username + '/list.json', auth=(RAVELRY_ACCESS_KEY, RAVELRY_PERSONAL_KEY))
        return r.json()
