from db import db

class DomainFeatureSet(db.Model):
    __tablename__ = 'domain_full_featureset'
    id=db.Column(db.Integer, primary_key=True)
    RegistryDate_year=db.Column(db.Integer)
    RegistryDate_month=db.Column(db.Integer)
    RegistryDate_day=db.Column(db.Integer)
    ExpirationDate_year=db.Column(db.Integer)
    ExpirationDate_month=db.Column(db.Integer)
    ExpirationDate_day=db.Column(db.Integer)
    HostCountry=db.Column(db.String(8))
    DomainAge=db.Column(db.Integer)
    URLType=db.Column(db.Integer)