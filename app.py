from flask import Flask, render_template, request, jsonify
from ocr_processor import process_ocr
from database import create_ocr_record, get_ocr_data, update_ocr_data, delete_ocr_record,db,db_config

app = Flask(__name__)
app.config.update(db_config)
db.init_app(app)

#welcome page for the users
@app.route('/')
def index():
    return render_template('index.html')

#page for uploading the identity cards for the users
@app.route('/upload',methods = ['POST','GET'])
def upload():
    if 'file' not in request.files:
        print ('file')
        output = jsonify({"error": "No file part"}), 400
        return output
    
    file = request.files['file']

    if file.filename == '':
        output = jsonify({"error": "Invalid file"}), 400
        return output

    try:
        result = process_ocr(file.read())
        create_ocr_record(result)
        output = jsonify(result)
        return output
    except Exception as e:
        output = jsonify({"error": str(e)}), 500
        return output

#page for the checking the already fed data into the database
@app.route('/history', methods=['POST'])
def history():
    date_of_birth = request.form.get('date_of_birth')
    identification_number = request.form.get('identification_number')
    output = jsonify(get_ocr_data(date_of_birth,identification_number))
    return render_template('history.html', output)
    

#page for deleting any record in the database
@app.route('/delete', methods=['DELETE'])
def delete_record():
    identification_number = request.form.get('identification_number')
    delete_ocr_record(identification_number)
    output = jsonify({"message": f"Record {identification_number} deleted successfully"})
    return render_template('delete.html',output)


#page for updating any data in the database
@app.route('/update',methods=['POST'])
def update_record(identification_number,result):
    old_identification_number = request.form.get('old_identification_number')
    new_name = request.form.get('new_name')
    new_last_name = request.form.get('new_last_name')
    new_identification_number = request.form.get('new_identification_number')
    new_date_of_issue = request.form.get('new_date_of_issue')
    new_date_of_expiry = request.form.get('new_date_of_expiry')
    new_date_of_birth = request.form.get('new_date_of_birth')
    delete_ocr_record (old_identification_number)
    result = {
            "id_number": new_identification_number,
            "name": new_name,
            "last_name": new_last_name,
            "date_of_birth": new_date_of_birth,
            "date_of_issue": new_date_of_issue,
            "date_of_expiry": new_date_of_expiry,
        }
    create_ocr_record(result)
    output = jsonify(result)
    return render_template('update.html',output)

if __name__ == '__main__':
    app.run(debug=True)
