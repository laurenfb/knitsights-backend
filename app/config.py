import os
from os.path import join, dirname
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

USERNAME = os.environ['USERNAME']
PASSWORD = os.environ['PASSWORD']

RAVELRY_ACCESS_KEY = os.environ['RAVELRY_ACCESS_KEY']
RAVELRY_PERSONAL_KEY = os.environ['RAVELRY_PERSONAL_KEY']

SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

TOP_LEVEL = ["clothing", "accessories", "home",
"toys and hobbies", "pet", "components"]

INTIMATE = ["bra", "pasties", "underwear"]
SWEATER = ["cardigan", "pullover"]
TOPS =["sleeveless top", "strapless top", "tee"]
BAG = ["backpack", "clutch", "drawstring", "duffle", "laptop", "market bag (slouchy)", "messenger", "money", "purse", "tote", "wristlet"]
SOCKS = ["ankle", "knee-highs", "mid-calf", "thigh-high", "toeless", "tube"]
HAT = ["balaclava", "beanie, toque", "beret, tam", "billed", "bonnet", "brimmed", "cloche", "earflap", "pixie", "stocking", "yarmulke"]
JEWELRY = ["ankle", "bracelet", "brooch", "earrings", "necklace", "ring"]
BLANKET = ["baby blanket", "bedspread", "throw"]
HOBBIES = ["ball", "blocks", "costume", "craft", "doll clothes", "food", "game", "mature content", "mobile", "puppet", "softies", "crochet hook holder", "needle holder", "pin cushion", "tape measure cover", "animal", "doll", "plant", "vehicle", "costume"]

CAT_W_PARENT = INTIMATE + SWEATER + TOPS + BAG + SOCKS + HAT + JEWELRY + BLANKET + HOBBIES

# if it's one of these, it needs to be something different than the parent.
# "gloves/mittens"
HANDS = ["convertible", "cuffs", "fingerless gloves/mitts", "gloves", "mittens", "muff"]
# "misc neckwear"
NECK = ["bib", "cape", "collar", "necktie"]
# "misc headwear"
HEAD = ["earwarmers", "eye mask", "hair accessories", "headband", "headwrap", "kerchief", "snood"]
# "home items"
HOME = ["bath mitt", "scrubber", "towel", "washcloth / dishcloth", "bookmark", "coaster", "containers", "automobile", "bathroom", "book cover", "coffee / tea pot", "cup / mug", "electronics", "food cozy", "glasses case", "hanger cover", "hot water bottle", "lip balm", "mature content toys", "sports equipment", "tissue box cover", "curtain", "christmas stocking", "doily", "hanging ornament", "ornamental flower", "picture frame", "wall hanging", "wreath", "lampshade", "medical", "pillow", "potholder", "rug", "sachet", "napkin", "placemat", "table runner", "tablecloth", "cleaning", "cozy", "decorative", "table setting"]
# "pet items"
PET_ITEMS = ["accessory", "bedding", "clothing", "other", "toys"]
# "knit components"
KNIT_COMPONENTS = ["afghan block", "applique / embellishment", "button", "chart", "edging", "floral block", "frog", "insertion", "other", "stitch pattern", "tutorial"]
# "socks"
MISC_SOCKS = ["booties", "legwarmers", "slippers", "socks", "spats"]


SQLALCHEMY_TRACK_MODIFICATIONS = False

ACCEPTABLE_REFERERS = ['http://localhost:8081', 'https://laurenfb.github.io/knitsights', 'https://laurenfb.github.io']
