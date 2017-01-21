import requests
from config import *
from app import db
from models import *
from datetime import date, timedelta, datetime

URL = 'https://api.ravelry.com/'

class APIWrapper:
    @staticmethod
    def import_user(current_username):
        r = requests.get(URL + 'projects/' + current_username + '/list.json', auth=(RAVELRY_ACCESS_KEY, RAVELRY_PERSONAL_KEY))

        user_info = requests.get(URL + "current_user.json", auth=(RAVELRY_ACCESS_KEY, RAVELRY_PERSONAL_KEY))

        user = User.query.filter_by(name = current_username).first()

        if r.status_code == 200:
            if user is None:
                if user_info.json()["user"]["large_photo_url"] is None:
                    photo_url = "http://placebeyonce.com/400-400"
                else:
                    photo_url = user_info.json()["user"]["large_photo_url"]
                user = User(name = current_username, email = "not sure how we're getting this", photo_url = photo_url, imported = True)
                db.session.add(user)
                db.session.commit()
            return_json = {"clusters": APIWrapper.sort_projects(r.json()["projects"], user.id)} #user.id is available after the user has been saved.
            # print return_json
            return return_json
        else:
            return r.status_code

    @staticmethod
    def sort_projects(projects, userID):
        # I want the projects to come back as an array.
        to_return = []
        for project in projects:
            # project must be finished. 2 is Rav's project_status_id for finshed. 1 is WIP, 3 is hibernating, 4 is frogged, in case that matters later.
            # also, the project needs to not already exist in the database.
            # print project["name"]
            if project["project_status_id"] == 2 and not APIWrapper.is_already_saved(project):
                # it will either have a pattern, or not have a pattern. deal with the projects that don't belong to a pattern first.
                if project["pattern_name"] is None: # json conversion  in requests makes None into None
                    APIWrapper.sort_proj_no_pattern(project, userID)
                else:
                    APIWrapper.sort_proj_with_pattern(project, userID)
        # then return a list of clusters with projects as lists inside of those.
        clusters = Cluster.query.filter_by(user_id = userID).all()
        for cluster in clusters:
            to_return.append({"name": cluster.name, "projects": [project.as_dict() for project in Project.query.filter_by(cluster_id = cluster.id).all() if project.time_in_days is not None]})
        return to_return

    @staticmethod
    def is_already_saved(project):
        database_project = Project.query.filter_by(rav_id = project["id"]).first()
        if database_project is None:
            return False
        else:
            return True

    @staticmethod
    def sort_proj_no_pattern(project, userID):
        # look for a cluster with title misc belonging to this user
        misc_cluster = Cluster.query.filter_by(user_id = userID, name="misc").first()
        if misc_cluster is None:
            # if they don't yet have one, make the cluster.
            misc_cluster = Cluster(name = "misc", user_id = userID, avg_days = None)
            db.session.add(misc_cluster)
            db.session.commit()
        # now the misc cluster is saved, so it has an ID. use that to make a new project in the database, using the cluster's ID
        project = Project(name = project["name"], photo_url = APIWrapper.photo_check(project), time_in_days = APIWrapper.calc_time_in_days(project), user_id = userID, cluster_id = misc_cluster.id, pattern_id = None, rav_id = project["id"])
        db.session.add(project)
        db.session.commit()

    @staticmethod
    def sort_proj_with_pattern(project, userID):
        #  get the project's pattern id,
        pattern_id = project["pattern_id"]
        # check to see if that pattern is in the database. if it's not, call the Rav API and put it in the database.
        pattern = Pattern.query.filter_by(id = pattern_id).first()
        if pattern is None:
            pattern = APIWrapper.single_pattern_call(pattern_id)
            if type(pattern) is not int: # returns error code if it doesn't go through.
                db.session.add(pattern)
        # pattern is already in the database
        else:
            # check to see if there is a cluster with that name under the user's name. cluster names are based on pattern categories.
            cluster = Cluster.query.filter_by(user_id = userID, name = pattern.category).first()
            # if there is not, make the cluster and give the the appropriate name
            if cluster is None:
                cluster = Cluster(name = pattern.category, user_id = userID, avg_days = None)
                # add it to the session, save that session so that I can use that cluster's ID to make the project.
                db.session.add(cluster)
                db.session.commit()
            # now the cluster does exist, even if I just had to make it, so use that cluster ID to make the project.
            new_project = Project(name = project["name"], photo_url = APIWrapper.photo_check(project), time_in_days = APIWrapper.calc_time_in_days(project), user_id = userID, cluster_id = cluster.id, pattern_id = pattern.id, rav_id = project["id"])
            db.session.add(new_project)
        db.session.commit()

    @staticmethod
    def single_pattern_call(pattern_id):
        r = requests.get(URL + "patterns/" + str(pattern_id) + ".json", auth=(RAVELRY_ACCESS_KEY, RAVELRY_PERSONAL_KEY))
        if r.status_code == 200:
            if len(r.json()["pattern"]["pattern_categories"]) > 0:
                category = APIWrapper.get_pattern_type(r.json()["pattern"]["pattern_categories"][0])
            else:
                category = "misc"
            if r.json()["pattern"]["name"] is None or r.json()["pattern"]["name"].lower() is "none":
                name = r.json()["pattern"]["permalink"].lower()
            else:
                name = r.json()["pattern"]["name"]
            pattern = Pattern(id = pattern_id, name = name, category = category)
            return pattern
        else:
            return r.status_code

    @staticmethod
    def get_pattern_type(pattern_category):
        name = pattern_category["name"].lower()
        if name == "other":
            category = APIWrapper.deal_with_other(pattern_category)
        elif name in HOBBIES:
            category = "toys and hobbies"
        elif name in HANDS:
            category = "gloves / mittens"
        elif name in NECK:
            category = "misc neckwear"
        elif name in HEAD:
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

    @staticmethod
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

    @staticmethod
    def calc_time_in_days(project):
        beginning = project["started"]
        end = project["completed"]
        # if they didn't set a date, it will be None.
        if beginning is None or end is None:
            return None
        else:
            beg_obj = datetime.strptime(beginning, '%Y/%m/%d').date()
            end_obj = datetime.strptime(end, '%Y/%m/%d').date()
            between = (end_obj - beg_obj).days
            return between

    @staticmethod
    def photo_check(project):
        if project["first_photo"] is None:
            return "http://placebeyonce.com/250-250"
        else:
            return project["first_photo"]["square_url"]
