import requests
from config import RAVELRY_ACCESS_KEY, RAVELRY_PERSONAL_KEY
from app import db
from models import *

URL = 'https://api.ravelry.com/'

class APIWrapper:
    @staticmethod
    def import_user(current_username):
        r = requests.get(URL + 'projects/' + current_username + '/list.json', auth=(RAVELRY_ACCESS_KEY, RAVELRY_PERSONAL_KEY))

        user_info = requests.get(URL + "current_user.json", auth=(RAVELRY_ACCESS_KEY, RAVELRY_PERSONAL_KEY))

        user = User.query.filter_by(name = current_username).first()

        if r.status_code == 200:
            if user is None:
                user = User(name = current_username, email = "not sure how we're getting this", photo_url = user_info.json()["user"]["large_photo_url"], imported = True)
                db.session.add(user)
                db.session.commit()
            # return {"clusters": sort_projects(r.json()["projects"], user.id)} #user.id is available after the user has been saved.
            return r.json()["projects"]
        else:
            return r.status_code


    def sort_projects(projects, userID):
        ### @TODO this is 100% non fucntional rn, but need to get the projects as they show up and save them in the database. also save user, and clusters.
        to_return = []
        for project in projects:
            # project must be finished.
            if project["status_name"] == "Finished":
                # it will either have a pattern, or not have a pattern.
                if project["pattern_name"] == "null": # or None? or null with no quotes?
                    # if there's no cluster called misc for this user...
                    misc_cluster = Cluster.query.filter_by(user_id = userID, name="misc").first()
                    if misc_cluster is None:
                        # make the cluster.
                        misc_cluster = Cluster(name = "misc", user_id = userID, avg_days = None)
                        db.session.add(misc_cluster)
                        db.session.commit()
                        # now the misc cluster is saved, so it has an ID. use that to make a new project in the database, using the cluster's ID
                        project = Project(name = project["name"], photo_url = project["square_url"], time_in_days = calc_time_in_days(project), user_id = userID, cluster_id = misc_cluster.id, pattern_id = None)
                        db.session.add(project)
                else:
                    # get the project's pattern id,
                    # check to see if there is a cluster with that name under the user's name.
                    # if there is not, make the cluster and give the the appropriate name
                    # if there is, make the project in the database and add it to the appropriate cluster

                    project = Project(name = project["name"], photo_url = project["square_url"], time_in_days = calc_time_in_days(project), user_id = userID, cluster_id = cluster.id, pattern_id = None)
                    db.session.add(project)
        db.session.commit()




    def get_pattern_type(pattern_category):
        name = pattern_category["name"].lower()
        if name == "other":
            category = deal_with_other(pattern_category)
        elif name in HOBBIES:
            category = "toys and hobbies"
        elif name in HANDS:
            category = "gloves / mittens"
        elif name in NECK:
            category = "misc neckwear"
        elif name in HEADWEAR:
            category = "misc headwear"
        elif name in HOME:
            category = "home items"
        elif name in PET_ITEMS:
            category = "pet items"
        elif name in KNIT_COMPONENTS:
            category = "knit components"
        elif name in MISC_SOCKS:
            category = "socks"
        elif name in CAT_W_PARENT:
            if pattern_category["parent"]["name"].lower() in TOP_LEVEL:
                category = name
            else:
                category = pattern_category["parent"]["name"].lower()
        else:
            category = name
        return category

    def deal_with_other(pattern_category):
        parent = pattern_category['parent']['name'].lower()
        if parent not in TOP_LEVEL:
            if parent in ["cleaning", "cozy", "decorative", "table setting"]:
                category = "home items"
            elif parent in ["craft", "softies"]:
                category = "toys and hobbies"
            elif parent == "neck / torso":
                category = "misc headwear"
            elif parent == "hands":
                category = "gloves / mittens"
            elif parent == "feet / legs":
                category = "socks"
            else:
                category = "misc"
        else:
            category = pattern_category['name'].lower()
        return category

    def calc_time_in_days(project):
        return 10
# #
# user = User.query.filter_by(name='laureneliz').first()
# print user is None
# clusters = Cluster.query.filter_by(user_id = user.id, name="misc").first()
# print clusters
# print len(clusters)
# pattern = Pattern.query.filter_by(name='Hitchhiker').first()
# print pattern
# print pattern.name
#
# APIWrapper.import_user("laureneliz")
