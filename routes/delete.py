from flask import request, Blueprint
from basics import jsonify
from tools import detachDeleteNode

delete = Blueprint('delete', __name__)


@delete.route('/delete/node/detach', methods=['POST'])
def delete_node():
    response = request.get_json()
    properties = response.get('properties', {})
    labels = response.get('labels', [])
    detachDeleteNode(properties, labels)

    return jsonify({'status': 'success'})
