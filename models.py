from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class MedicalInfo(db.Model):
    __tablename__ = 'medical_info'
    medical_id = db.Column(db.String(100), primary_key=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    blood_type = db.Column(db.String(10))
    allergies = db.Column(db.String(200))
    medical_conditions = db.Column(db.String(200))
    medications = db.Column(db.String(200))
    emergency_contact = db.Column(db.String(50))
    primary_physician = db.Column(db.String(100))
    insurance_info = db.Column(db.String(200))
    organ_donor = db.Column(db.Boolean)
    other_info = db.Column(db.String(200))
    nfc_tags = db.relationship('NfcTag', backref='medical_info', lazy=True)

class NfcTag(db.Model):
    __tablename__ = 'nfc_tags'
    tag_id = db.Column(db.String(100), primary_key=True)
    medical_id = db.Column(db.String(100), db.ForeignKey('medical_info.medical_id'), nullable=False)
