from flask import Flask, render_template, request, jsonify
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import InputRequired
from werkzeug.utils import secure_filename
import os
import json
from ocr_processor import process_ocr
from database import create_ocr_record, get_ocr_data, update_ocr_data, delete_ocr_record,db,db_config,get_ocr_data_identification,get_ocr_data_dob

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static'
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
    output ={}
    if form.validate_on_submit():
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename)))
        try:
            result = process_ocr(file.filename)
            print (result)
            create_ocr_record(result)
            output = result
        except Exception as e:
            output = jsonify({"error": str(e)}), 500
    return render_template ('index.html',form=form, output = output)

#page for the checking the already fed data into the database
@app.route('/history', methods=["POST",'GET'])
def history():
    date_of_birth = request.form.get('date_of_birth')
    identification_number = request.form.get('identification_number')
    result={}
    if date_of_birth == None:
        output = get_ocr_data_identification(identification_number)
        result = output
        msg = "No data found"
        result = output if len(output) > 0 else msg
    elif identification_number == None:
        output = get_ocr_data_dob(date_of_birth)
        result = output
        msg = "No data found"
        result = output if len(output) > 0 else msg
    else:
        output = get_ocr_data(date_of_birth,identification_number)
        result = output
        msg = "No data found"
        result = output if len(output) > 0 else msg
    return render_template('history.html',output = result)
    

#page for deleting any record in the database
@app.route('/delete', methods=["DELETE","POST",'GET'])
def delete_record():
    output =""  
    if request.method != 'GET':
        identification_number = request.form.get('identification_number')
        if(delete_ocr_record(identification_number)):
            output = "Record deleted successfully"
        else:
            output = "Record not found"
    data =output
    return render_template("delete.html",data = data)


#page for updating any data in the database
@app.route('/update',methods=['GET',"POST"])
def update_record():
    output=""
    if request.method != "GET":
        old_identification_number = request.form.get('old_identification_number')
        value1 = request.form.get('value1')
        value2 = request.form.get('value2')
        value3 = request.form.get('value3')
        value4 = request.form.get('value4')
        value5 = request.form.get('value5')
        value6 = request.form.get('value6')
    
        name={}
        if value1 is not None:
            name['name'] = value1
        else:
            name['name'] = "None"
        if value2 is not None:
            name['last_name'] = value2
        else:
            name['last_name'] = "None"
        if value3 is not None:
            name['id_number'] = value3
        else:
            name['id_number'] = "None"
        if value4 is not None:
            name['date_of_issue'] = value4
        else:
            name['date_of_issue'] = "None"
        if value5 is not None:
            name['date_of_expiry'] = value5
        else:
            name['date_of_expiry'] = "None"
        if value6 is not None:
            name['date_of_birth'] = value6
        else:
            name['date_of_birth'] = "None"
        
        result = update_ocr_data(old_identification_number,name)
        output = result
    return render_template('update.html',data=output)

if __name__ == '__main__':
    app.run()
