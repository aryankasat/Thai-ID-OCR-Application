from flask import Flask, render_template, request, jsonify
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, StringField, DateField,IntegerField
from wtforms.validators import InputRequired, DataRequired
from ocr_processor import process_ocr
from database import create_ocr_record, get_ocr_data, update_ocr_data, delete_ocr_record,db,db_config

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config.update(db_config)
db.init_app(app)

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

@app.route('/',methods=["POST",'GET'])

#page for uploading the identity cards for the users
@app.route('/upload',methods = ["POST",'GET'])
def upload():

    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        try:
            result = process_ocr(file)
            create_ocr_record(result)
            output = jsonify(result)
            return output
        except Exception as e:
            output = jsonify({"error": str(e)}), 500
        return output
    return render_template ('index.html',form = form)

#page for the checking the already fed data into the database
@app.route('/history', methods=["POST",'GET'])
def history():
    date_of_birth = request.form.get('date_of_birth')
    identification_number = request.form.get('identification_number')
    output = jsonify(get_ocr_data(date_of_birth,identification_number))
    return render_template('history.html',data = output)
    

#page for deleting any record in the database
@app.route('/delete', methods=["DELETE","POST",'GET'])
def delete_record():
    identification_number = request.form.get('identification_number')
    delete_ocr_record(identification_number)
    output = jsonify({"message": f"Record {identification_number} deleted successfully"})
    return render_template('delete.html',data = output)


#page for updating any data in the database
@app.route('/update',methods=["POST",'GET'])
def update_record():
    old_identification_number = request.form.get('old_identification_number')
    value1 = request.form.get('value1')
    value2 = request.form.get('value2')
    value3 = request.form.get('value3')
    value4 = request.form.get('value4')
    value5 = request.form.get('value5')
    value6 = request.form.get('value6')
    name={}
    if value1 is not None:
        name['Name'] = value1
    else:
        name['Name'] = " "
    if value2 is not None:
        name['Last_Name'] = value2
    else:
        name['Last_Name'] = " "
    if value3 is not None:
        name['Identification_number'] = value3
    else:
        name['Identification'] = " "
    if value4 is not None:
        name['Date_of_issue'] = value4
    else:
        name['Date_of_issue'] = " "
    if value5 is not None:
        name['Date_of_expiry'] = value5
    else:
        name['Date_of_expiry'] = " "
    if value6 is not None:
        name['Date_of_birth'] = value6
    else:
        name['Date_of_birth'] = " "
    
    result = update_ocr_data(old_identification_number,name)
    output = jsonify(result)
    return render_template('update.html',data = output)

if __name__ == '__main__':
    app.run(debug=True)
