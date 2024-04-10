from werkzeug.utils import secure_filename
from basics import grid_fs
from flask import request, redirect, Blueprint, jsonify, stream_with_context, Response
from warnings import warn
import re

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
        # Buscar el archivo en GridFS por su nombre de archivo
        file_data = grid_fs.find_one({'filename': filename})
        if file_data is None:
            return jsonify({'status': 'error', 'message': 'Archivo no encontrado'})

        # Obtener el ID del archivo
        file_id = file_data._id

        # Obtener el archivo como un stream (GridOut)
        file = grid_fs.get(file_id)

        print("Enviando...")

        # Configurar la respuesta para streaming del archivo
        response = Response(stream_with_context(file),
                            content_type=file_data.content_type,
                            headers={"Content-Disposition": f"inline; filename={file_data.filename}"})

        print("Mandando...")

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


@gridR.route('/stream/<filename>')
def stream_video(filename):
    try:
        # Buscar el archivo en GridFS por su nombre de archivo
        file_data = grid_fs.find_one({'filename': filename})
        if file_data is None:
            return jsonify({'status': 'error', 'message': 'Archivo no encontrado'}), 404

        # Obtener el ID del archivo
        file_id = file_data._id

        # Obtener el archivo como un stream (GridOut)
        file = grid_fs.get(file_id)

        # Obtener información sobre el tamaño del archivo
        file_size = file_data.length

        # Determinar el rango de bytes solicitado por el cliente
        range_header = request.headers.get('Range', None)
        start_range, end_range = parse_range_header(range_header, file_size)

        # Calcular la longitud del contenido a transmitir
        if start_range is None:
            start_range = 0
        if end_range is None or end_range >= file_size:
            end_range = file_size - 1
        length = end_range - start_range + 1

        # Establecer los encabezados de respuesta para el rango de bytes
        headers = {
            'Content-Type': file_data.content_type,
            'Content-Length': length,
            'Accept-Ranges': 'bytes',
            'Content-Range': f"bytes {start_range}-{end_range}/{file_size}"
        }

        # Configurar la respuesta para streaming del contenido parcial (byte-range)
        response = Response(
            stream_with_context(generate_file_content(file, start_range, length)),
            status=206,  # Código de estado 206 para respuesta parcial
            headers=headers
        )

        return response

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


def parse_range_header(range_header, file_size):
    if not range_header:
        return None, None

    range_match = re.match(r'bytes=(\d+)-(\d*)', range_header)
    if range_match:
        start_range = int(range_match.group(1))
        end_range = int(range_match.group(2)) if range_match.group(2) else None
        if end_range and end_range >= file_size:
            end_range = file_size - 1
        return start_range, end_range

    return None, None


def generate_file_content(file, start_range, length):
    """Genera el contenido del archivo para transmitir."""
    if start_range is not None:
        file.seek(start_range)

    remaining_bytes = length
    while remaining_bytes > 0:
        # Lee los datos en fragmentos para transmitir por partes
        chunk_size = min(remaining_bytes, 1024 * 1024)  # Lee en fragmentos de hasta 1 MB
        data = file.read(chunk_size)
        if not data:
            break
        yield data
        remaining_bytes -= len(data)