from db import db
from models.FeatureSets import DomainFeatureSet, LexicalFeatureSet

import csv, sqlite3
from flask_restful import reqparse
from flask import current_app as app

DOMAIN_CREATE_SQL = "CREATE TABLE IF NOT EXISTS domain_full_featureset (id integer primary key AUTOINCREMENT, RegistryDate_year,RegistryDate_month,RegistryDate_day,ExpirationDate_year,ExpirationDate_month,ExpirationDate_day,HostCountry,DomainAge,URLType);"
LEXICAL_CREATE_SQL = "CREATE TABLE IF NOT EXISTS lexical_full_featureset (id integer primary key AUTOINCREMENT, URLLength,HostLength,TLDLength,DotCount,DashCount,AtSymbolCount,PercentSymbolCount,EqualsSymbolCount,QuestionMarkCount,DigitCount,UniqueCharCount,URLType);"

def setup_db(feature: str):
    dataset_count = 0
    try:
        dataset_count=db.session.execute(f'SELECT COUNT(*) FROM {feature}_full_featureset').first()[0]
    except Exception as error:
        create_db(feature=feature)

    if (dataset_count == 0):
        populate_db(feature=feature)

def create_db(feature: str):
    con = sqlite3.connect('/Users/chrismclearnon/Developer/QUB-CSC3032-FYP/src/ml-demo-app/api/db/datasets.db')
    cur = con.cursor()        
    if (feature == 'domain'):
        cur.execute(DOMAIN_CREATE_SQL)
    elif (feature == 'lexical'):
        cur.execute(LEXICAL_CREATE_SQL)
    con.commit()
    con.close()
    print(f'[+] {feature}_full_featureset.db created')

def populate_db(feature: str):
    con = sqlite3.connect('/Users/chrismclearnon/Developer/QUB-CSC3032-FYP/src/ml-demo-app/api/db/datasets.db')
    cur = con.cursor() 

    if (feature == 'domain'):
        with open(app.config['DOMAIN_DATA'],'r') as fin:
            dr = csv.DictReader(fin)
            dataset = [(str(i['RegistryDate_year']),
                        i['RegistryDate_month'],
                        i['RegistryDate_day'],
                        i['ExpirationDate_year'],
                        i['ExpirationDate_month'],
                        i['ExpirationDate_day'],
                        i['HostCountry'],
                        i['DomainAge'],
                        i['URLType']) for i in dr]

        cur.executemany("INSERT INTO domain_full_featureset (RegistryDate_year,RegistryDate_month,RegistryDate_day,ExpirationDate_year,ExpirationDate_month,ExpirationDate_day,HostCountry,DomainAge,URLType) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);", dataset)
    elif (feature == 'lexical'):
        with open(app.config['LEXICAL_DATA'],'r') as fin:
            dr = csv.DictReader(fin)
            dataset = [(str(i['URLLength']),
                        i['HostLength'],
                        i['TLDLength'],
                        i['DotCount'],
                        i['DashCount'],
                        i['AtSymbolCount'],
                        i['PercentSymbolCount'],
                        i['EqualsSymbolCount'],
                        i['QuestionMarkCount'],
                        i['DigitCount'],
                        i['UniqueCharCount'],
                        i['URLType']) for i in dr]

        cur.executemany("INSERT INTO lexical_full_featureset (URLLength,HostLength,TLDLength,DotCount,DashCount,AtSymbolCount,PercentSymbolCount,EqualsSymbolCount,QuestionMarkCount,DigitCount,UniqueCharCount,URLType) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", dataset)
    con.commit()
    con.close()
    print(f'[+] {feature}_full_featureset.db populated')