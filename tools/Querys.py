from .Classes import transFormObject
from typing import LiteralString
from basics import neo4j_driver
from neo4j import Result
from basics import jsonify


def makeQuery(query: LiteralString = 'MATCH (n) RETURN n', params=None, listOffIndexes=None):
    if listOffIndexes is None:
        listOffIndexes = ['n']
    if params is None:
        params = {}

    with neo4j_driver.session() as session:
        nodes: Result = session.run(query, params)
        records = []
        for n in nodes:
            records.append(tuple([transFormObject(n[index]) for index in listOffIndexes]))
        return records


def convertJson(records):
    ret = []
    if len(records[0]) > 1:
        for record in records:
            ret.append([r.to_json() for r in record])
    else:
        for record in records:
            ret.append(record[0].to_json())
    return jsonify(ret)
