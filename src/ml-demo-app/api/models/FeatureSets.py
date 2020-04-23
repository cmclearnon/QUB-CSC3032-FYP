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

class LexicalFeatureSet(db.Model):
    __tablename__ = 'lexical_full_featureset'
    id=db.Column(db.Integer, primary_key=True)
    URLLength=db.Column(db.Integer)
    HostLength=db.Column(db.Integer)
    TLDLength=db.Column(db.Integer)
    DotCount=db.Column(db.Integer)
    DashCount=db.Column(db.Integer)
    AtSymbolCount=db.Column(db.Integer)
    PercentSymbolCount=db.Column(db.Integer)
    EqualsSymbolCount=db.Column(db.Integer)
    QuestionMarkCount=db.Column(db.Integer)
    DigitCount=db.Column(db.Integer)
    UniqueCharCount=db.Column(db.Integer)
    URLType=db.Column(db.Integer)