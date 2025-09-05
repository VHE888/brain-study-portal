from flask_sqlalchemy import SQLAlchemy
from datetime import date

# 1. Initialize SQLAlchemy. We do this here so other files can import it.
db = SQLAlchemy()

# --- DATABASE MODELS ---
# All your model classes are now in this file.

# Junction table
dataset_region_association = db.Table('dataset_region_association',
    db.Column('dataset_id', db.Integer, db.ForeignKey('dataset.did'), primary_key=True),
    db.Column('region_id', db.Integer, db.ForeignKey('region.rid'), primary_key=True)
)

class Publication(db.Model):
    __tablename__ = 'publication'
    pid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    publication_date = db.Column(db.Date, nullable=True)
    journal = db.Column(db.String(150), nullable=True)
    datasets = db.relationship('Dataset', back_populates='publication', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Publication PID: {self.pid}>'

class Dataset(db.Model):
    __tablename__ = 'dataset'
    did = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(500), nullable=True)
    pid = db.Column(db.Integer, db.ForeignKey('publication.pid'), nullable=False)
    sid = db.Column(db.Integer, db.ForeignKey('species.sid'), nullable=False)
    publication = db.relationship('Publication', back_populates='datasets')
    species = db.relationship('Species', back_populates='datasets')
    regions = db.relationship('Region', secondary=dataset_region_association, back_populates='datasets')

    def __repr__(self):
        return f'<Dataset DID: {self.did}>'

class Species(db.Model):
    __tablename__ = 'species'
    sid = db.Column(db.Integer, primary_key=True)
    species_name = db.Column(db.String(100), unique=True, nullable=False)
    datasets = db.relationship('Dataset', back_populates='species')

    def __repr__(self):
        return self.species_name

class Region(db.Model):
    __tablename__ = 'region'
    rid = db.Column(db.Integer, primary_key=True)
    brain_region_name = db.Column(db.String(150), unique=True, nullable=False)
    datasets = db.relationship('Dataset', secondary=dataset_region_association, back_populates='regions')

    def __repr__(self):
        return self.brain_region_name