from db import db
from models.DomainFullFeatureSet import DomainFullFeatureSet

import csv, sqlite3
from flask_restful import reqparse

def setup_db():
    try:
        dataset_count=db.session.execute('SELECT COUNT(*) FROM domain_full_featureset').first()[0]
    except Exception as error:
        create_db()

    if dataset_count == 0 {
        populate_db()
    }

def create_db():
    con = sqlite3.connect('/Users/chrismclearnon/Developer/QUB-CSC3032-FYP/src/ml-demo-app/api/db/datasets.db')
    cur = con.cursor()        
    cur.execute("CREATE TABLE IF NOT EXISTS domain_full_featureset (RegistryDate_year,RegistryDate_month,RegistryDate_day,ExpirationDate_year,ExpirationDate_month,ExpirationDate_day,HostCountry,DomainAge,URLType);")
    con.commit()
    con.close()
    print('+ domain_full_featureset.db created')

def populate_db():
    con = sqlite3.connect('/Users/chrismclearnon/Developer/QUB-CSC3032-FYP/src/ml-demo-app/api/db/datasets.db')
    cur = con.cursor() 
    with open('/Users/chrismclearnon/Developer/QUB-CSC3032-FYP/src/data/domain_full_featureset.csv','r') as fin: # `with` statement available in 2.5+
    dr = csv.DictReader(fin) # comma is default delimiter
    dataset = [(str(i['RegistryDate_year']),
                i['RegistryDate_month'],
                i['RegistryDate_day'],
                i['ExpirationDate_year'],
                i['ExpirationDate_month'],
                i['ExpirationDate_day'],
                i['HostCountry'],
                i['DomainAge'],
                i['URLType']) for i in dr]

    db.engine.execute(DomainFullFeatureSet.__table__.insert(), dataset)
    #cur.executemany("INSERT INTO domain_full_featureset (RegistryDate_year,RegistryDate_month,RegistryDate_day,ExpirationDate_year,ExpirationDate_month,ExpirationDate_day,HostCountry,DomainAge,URLType) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);", dataset)
    con.commit()
    con.close()
    print('+ domain_full_featureset.db populated')