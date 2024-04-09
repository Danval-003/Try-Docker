from basics import jsonify, neo4j_driver
from flask import request, Blueprint
from tools import makeQuery, format_properties


read = Blueprint('read', __name__)


@read.route('/search/node', methods=['POST'])
def searchNode():
    response = request.get_json()
    properties = response.get('properties', {})
    labels = response.get('labels', [])

    query = f"MATCH (n:{':'.join(labels)} {format_properties(properties)}) RETURN n"

    results = makeQuery(query, listOffIndexes=['n'])

    nodes = [n[0].to_json() for n in results]

    return jsonify({'status': 'success', 'nodes': nodes})
