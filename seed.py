'''Script to seed database for INVESTABLE app'''
from model import User, Property, connect_to_db, db
from server import app
from csv import reader
from random import randint

def seed_users():
    '''seed users from investables.csv into database '''
    for i, row in enumerate(open('data/investables_db.csv')):
        row = row.rstrip()
        first_name, last_name, email = row.split('|')
        user = User(first_name=first_name, last_name=last_name, email=email)
        db.session.add(user)
    db.session.commit()

def seed_properties():
    '''load property data from Redfin combined.csv into database'''
    RATE = 0.045
    INSURANCE = 2000
    with open('data/combined.csv') as f:
        # to skip the first row of headings
        next(f)
        data = reader(f, delimiter=',')
        for row in data:
             #convert from string to list
            property_data = ','.join(row).split(',')
            sample_properties = Property(
            user_id = randint(1, 9),
            price = int(property_data[7]),
            down_payment = round(int(property_data[7]) * 0.2, 2),
            interest_rate = RATE,
            mortgage = round(int(property_data[7]) * 0.0037, 2),
            closing_costs = round(int(property_data[7]) * 0.01, 2), 
            rehab = round(int(property_data[7]) * 0.01, 2),
            monthly_rent = round(int(property_data[7]) * 0.008, 2),
            property_taxes = round((int(property_data[7]) * 0.015)/12, 2),
            insurance = round(int(INSURANCE)/12, 2),
            hoa = max(int(row[16]), 15)
            
            )
            db.session.add(sample_properties)
        db.session.commit()
    



if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()
    seed_users()
    seed_properties()