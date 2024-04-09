from basics import neo4j_driver
from neo4j import Result
from basics import jsonify
from .Classes import NodeD, transFormObject, _format_properties
from typing import List


def createNode(labels: List[str], params=None, merge=False):
    if params is None:
        params = {}

    with neo4j_driver.session() as session:
        cypher_query = f"CREATE (node:{':'.join(labels)} {_format_properties(params)})"
        if merge:
            cypher_query = f"MERGE (node:{':'.join(labels)} {_format_properties(params)})"
        session.run(cypher_query)


def createRelationship(node1: NodeD, node2: NodeD, typeR: str, properties=None, merge=True):
    if properties is None:
        properties = {}

    with neo4j_driver.session() as session:
        cypher_query = f"MATCH (a{':' if len(node1.labels) > 0 else ''}{':'.join(node1.labels)} " \
                       f"{_format_properties(node1.properties)}) " \
                       f"MATCH (b{':' if len(node2.labels) > 0 else ''}{':'.join(node2.labels)}" \
                       f" {_format_properties(node2.properties)}) " \
                       f"CREATE (a)-[r:{typeR} {_format_properties(properties)}]->(b)"
        if merge:
            cypher_query = f"MATCH (a{':' if len(node1.labels) > 0 else ''}{':'.join(node1.labels)}" \
                           f"{_format_properties(node1.properties)}) " \
                           f"MATCH (b{':' if len(node2.labels) > 0 else ''}{':'.join(node2.labels)} " \
                           f"{_format_properties(node2.properties)}) " \
                           f"MERGE (a)-[r:{typeR} {_format_properties(properties)}]->(b)"
        session.run(cypher_query)


def makeQuery(query: str = 'MATCH (n) RETURN n', params=None, listOffIndexes=None):
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


def searchNode(labels: List[str], properties=None):
    if properties is None:
        properties = {}

    with neo4j_driver.session() as session:
        cypher_query = f"MATCH (node{':' if len(labels) > 0 else ''}{':'.join(labels)} " \
                       f"{_format_properties(properties)}) RETURN node"
        nodes = session.run(cypher_query)
        records = []
        for n in nodes:
            records.append(transFormObject(n['node']))
        return records


def convertJson(records):
    ret = []
    if len(records) == 0:
        return jsonify([])
    if len(records[0]) > 1:
        for record in records:
            ret.append([r.to_json() for r in record])
    else:
        for record in records:
            ret.append(record[0].to_json())
    return jsonify(ret)


def detachDeleteNode(properties=None, labels=None):
    if properties is None:
        properties = {}
    with neo4j_driver.session() as session:
        cypher_query = f"MATCH (node{':' if len(labels) > 0 else ''}{':'.join(labels)}" \
                       f" {_format_properties(properties)}) DETACH DELETE node"
        session.run(cypher_query)
