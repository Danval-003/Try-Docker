from flask import request, Blueprint
from basics import jsonify
from tools import detachDeleteNode

update = Blueprint('update', __name__)


@update.route('/update/node', methods=['POST'])
def update_node():
    response = request.get_json()
    properties = response.get('properties', {})
    labels = response.get('labels', [])
    detachDeleteNode(properties, labels)

    return jsonify({'status': 'success'})

