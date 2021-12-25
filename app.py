from flask import Flask, json, request, jsonify, make_response, send_file
import os
import urllib.request
from werkzeug.utils import secure_filename
from flask_cors import CORS
 
app = Flask(__name__)
CORS(app)
 
app.secret_key = "caircocoders-ednalan"
 
UPLOAD_FOLDER = 'savefiles/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['mp4', 'avi'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
 
@app.route('/')
def main():
    resp = send_file(os.path.join(app.config['UPLOAD_FOLDER'], "hw_out.mp4"),attachment_filename="hw_out.mp4", as_attachment=True)
    resp.status_code = 200
    resp.headers["message"] = jsonify("Files successfully uploaded")
    return resp
 
@app.route('/upload', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'files[]' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp
 
    files = request.files.getlist('files[]')
     
    errors = {}
    success = False
     
    for file in files:      
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            success = True
            print(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            errors[file.filename] = 'File type is not allowed'
 
    if success and errors:
        errors['message'] = 'File(s) successfully uploaded'
        resp = send_file(os.path.join(app.config['UPLOAD_FOLDER'], "hw_out.mp4"),attachment_filename="hw_out.mp4", as_attachment=True)
        resp.status_code = 500
        resp.headers["message"] = jsonify(errors)
        return resp
    if success:
        resp = send_file(os.path.join(app.config['UPLOAD_FOLDER'], "hw_out.mp4"),attachment_filename="hw_out.mp4", as_attachment=True)
        resp.status_code = 200
        resp.headers["message"] = jsonify("Files successfully uploaded")
        return resp
    else:
        resp = jsonify(errors)
        resp.status_code = 500
        return resp
 
if __name__ == '__main__':
    app.run(debug=True)