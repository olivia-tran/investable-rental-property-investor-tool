'''Script to seed database for INVESTABLE app'''
from model import User, Property,BlogPost, Comment, connect_to_db, db
from server import app
from csv import reader
from random import randint
from datetime import datetime


def seed_users():
    '''seed users from investables.csv into database '''
    for i, row in enumerate(open('data/investables_db.csv')):
        row = row.rstrip()
        first_name, last_name, email = row.split('|')
        user = User(first_name=first_name, last_name=last_name, email=email)
        db.session.add(user)
    db.session.commit()
    
    
def seed_blogs():
    '''seed blog posts from blogs.csv into database '''
    user_id = randint(1, 5)
    with open ('data/blogs.csv') as f:
        data = reader(f, delimiter=',')
        for row in data:
            blogs = ','.join(row).split(',')
            print(f'=======TITLE======{blogs}')
            posts = BlogPost(user_id= user_id, title=blogs[0], blog_content=blogs[1], created_at=datetime.now())
        db.session.add(posts)
    db.session.commit()

def seed_properties():
    '''load property data from Redfin combined.csv into database'''
    INSURANCE = 2000
    with open('data/combined.csv') as f:
        # to skip the first row of headings
        next(f)
        data = reader(f, delimiter=',')
        for row in data:
            # convert from string to list
            property_data = ','.join(row).split(',')
            sample_properties = Property(
                user_id=randint(1, 9),
                rent=min(
                    round(int(property_data[7]) * 0.008, 2), 5000),
                mortgage=round(int(property_data[7]) * 0.0037, 2),
                tax=round((int(property_data[7]) * 0.015)/12, 2),
                insurance=round(int(INSURANCE)/12, 2),
                hoa=max(int(row[16]), 15)
            )
            db.session.add(sample_properties)
        db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()
    seed_users()
    seed_properties()
