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
        query = query.filter(OCRRecord.ocr_result['identification_number']==identification_number)
    
    ocr_data = query.all()
    return ocr_data

#updating data in database
def update_ocr_data(record_id, value,name):
    query = OCRRecord.query
    record = query.filter (OCRRecord.ocr_result['identification_number'] == record_id)
    new_record = None
    r = record.all()
    if len(r) >=3:
        record_json = r[3]
        record_json_loads = json.loads(record_json)
        if record:
            record_json_loads.name = value
            db.session.commit()
        new_record = query.filter(OCRRecord.ocr_result['idetification_number'] == record_id)
    return new_record

#deleting data from database
def delete_ocr_record(record_id):
    record = OCRRecord.query.get(record_id)
    if record:
        db.session.delete(record)
        db.session.commit()