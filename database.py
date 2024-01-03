from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
db = SQLAlchemy()

db_uri = 'mysql://root:Aruboi2001!@localhost/ocr'

# Define the database configuration
db_config = {
    'SQLALCHEMY_DATABASE_URI': db_uri,
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
}

class OCRRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(10))
    ocr_result = db.Column(db.JSON)

#creation of new entry in the database
def create_ocr_record(result):
    record = OCRRecord(status="success", ocr_result=result)
    db.session.add(record)
    db.session.commit()

#retriving data from database
def get_ocr_data(date_of_birth,identification_number):
    query = OCRRecord.query

    if date_of_birth:
        query = query.filter(OCRRecord.ocr_result['date_of_birth']==date_of_birth)

    if identification_number:
        query = query.filter(OCRRecord.ocr_result['id_number']==identification_number)
    
    ocr_data = query.all()
    return ocr_data

def get_ocr_data_dob (date_of_birth):
    query = OCRRecord.query

    if date_of_birth:
        query = query.filter(OCRRecord.ocr_result['date_of_birth']==date_of_birth)
    
    ocr_data = query.all()
    return ocr_data

def get_ocr_data_identification(identification_number):
    query = OCRRecord.query

    if identification_number:
        query = query.filter(OCRRecord.ocr_result['id_number']==identification_number)
    
    ocr_data = query.all()
    return ocr_data

#updating data in database
def update_ocr_data(old_identification_number, name):
    query = OCRRecord.query

    if old_identification_number:
        query = query.filter(OCRRecord.ocr_result['id_number']==old_identification_number)
    
    ocr_data = query.all()
    new_record = None

    print (ocr_data)
    num = 0
    for r in ocr_data:
        num = r.id
    update = OCRRecord.query.get(num)
    print (update)
    if update:
        if name['name'] is not None:
            update.ocr_result['name'] = name['name']
            print ("aaaaaaaaaaaaaaaaaaaa")
        if name['last_name'] is not None:
            update.ocr_result['last_name'] = name['last_name']
        if name['id_number'] is not None:
            update.ocr_result['id_number'] = name['id_number']
        if name['date_of_birth'] is not None:
            update.ocr_result['date_of_birth'] = name['date_of_birth']
        if name['date_of_issue'] is not None:
            update.ocr_result['date_of_issue'] = name['date_of_issue']
        if name['date_of_expiry'] is not None:
            update.ocr_result['date_of_expiry'] = name['date_of_expiry']
        db.session.commit()
    query = query.filter(OCRRecord.ocr_result['id_number'] == old_identification_number)
    new_record = query.all()
    return new_record

#deleting data from database
def delete_ocr_record(identification_number):
    query = OCRRecord.query

    if identification_number:
        query = query.filter(OCRRecord.ocr_result['id_number']==identification_number)
    
    ocr_data = query.all()
    num = 0
    for i in ocr_data:
        num = i.id
    record = OCRRecord.query.get(num)
    if record:
        db.session.delete(record)
        db.session.commit()
        return True
    else:
        return False