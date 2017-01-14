import requests
from config import RAVELRY_ACCESS_KEY, RAVELRY_PERSONAL_KEY

URL = 'https://api.ravelry.com/'

class APIWrapper:
    @staticmethod
    def get_current_user_projects(current_username):
        r = requests.get(URL + 'projects/' + current_username + '/list.json', auth=(RAVELRY_ACCESS_KEY, RAVELRY_PERSONAL_KEY))
        if r.status_code == 200:
            return r.json()["projects"]
        else:
            return r.status_code

    #
    # def sort_projects(projects):
    #     for project in projects:
    #
    #
    #
    # def get_pattern_type(pattern_category):
    #     name = pattern_category["name"].lower()
    #     if name == "other":
    #         category = deal_with_other(pattern_category)
    #     elif name in HOBBIES:
    #         category = "toys and hobbies"
    #     elif name in HANDS:
    #         category = "gloves / mittens"
    #     elif name in NECK:
    #         category = "misc neckwear"
    #     elif name in HEADWEAR:
    #         category = "misc headwear"
    #     elif name in HOME:
    #         category = "home items"
    #     elif name in PET_ITEMS:
    #         category = "pet items"
    #     elif name in KNIT_COMPONENTS:
    #         category = "knit components"
    #     elif name in MISC_SOCKS:
    #         category = "socks"
    #     elif name in CAT_W_PARENT:
    #         if pattern_category["parent"]["name"].lower() in TOP_LEVEL:
    #             category = name
    #         else:
    #             category = pattern_category["parent"]["name"].lower()
    #     else:
    #         category = name
    #     return category
    #
    # def deal_with_other(pattern_category):
    #     parent = pattern_category['parent']['name'].lower()
    #     return "other"
