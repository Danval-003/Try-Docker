from flask import request
from basics import app, jsonify
from tools import createNode


@app.route('/create/node', methods=['POST'])
def create_node():
    response = request.get_json()
    properties = response.get('properties', {})
    labels = response.get('labels', [])
    merge = response.get('merge', False)

    createNode(labels, properties, merge)

    return jsonify({'status': 'success'})


