import csv
from app.app import db

# db.drop_all()
from app.models import Pattern

with open('seed_file.csv', 'rb') as csvfile:
    data = csv.reader(csvfile)
    for row in data:
        if Pattern.query.filter_by(id = int(row[2])) is None:
            pattern = Pattern(id = int(row[2]), name = row[0], category = row[1])
            db.session.add(pattern)

db.session.commit()
