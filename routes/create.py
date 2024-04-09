from flask import request, Blueprint
from basics import jsonify
from tools import createNode

create = Blueprint('create', __name__)


@create.route('/create/node', methods=['POST'])
def create_node():
    response = request.get_json()
    properties = response.get('properties', {})
    labels = response.get('labels', [])
    merge = response.get('merge', False)

    createNode(labels, properties, merge)

    return jsonify({'status': 'success'})


@create.route('/create/nodes', methods=['POST'])
def create_nodes():
    response = request.get_json()

    for node in response:
        properties = node.get('properties', {})
        labels = node.get('labels', [])
        merge = node.get('merge', False)

        createNode(labels, properties, merge)

    return jsonify({'status': 'success'})
