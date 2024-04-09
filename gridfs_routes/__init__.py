from gridfs import GridOut
from werkzeug.utils import secure_filename
from basics import grid_fs
from flask import request, redirect, Blueprint, jsonify, send_file
from warnings import warn

gridR = Blueprint('gridR', __name__)


@gridR.route('/upload', methods=['POST'])
def upload_file():
    warn('Entro')
    try:
        if 'file' not in request.files:
            warn('No file part')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)

        if file:
            filename = secure_filename(file.filename)
            content_type = file.content_type
            grid_fs.put(file, filename=filename, content_type=content_type)
            return jsonify({'status': 'success'})
    except Exception as e:
        warn(str(e))

    return jsonify({'status': 'error'})


@gridR.route('/download/<filename>')
def download_file(filename):
    print('Entro')
    try:
        file_data = grid_fs.find_one({'filename': filename})
        fileid = file_data._id
        file: GridOut = grid_fs.get(fileid)
        response = send_file(file, mimetype=file_data.content_type)
        return response
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


@gridR.route('/see/<filename>')
def see_file(filename):
    try:
        file = grid_fs.find_one({'filename': filename})
        return file.read()
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


@gridR.route('/delete/<filename>')
def delete_file(filename):
    try:
        file = grid_fs.find_one({'filename': filename})
        grid_fs.delete(file._id)
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})
