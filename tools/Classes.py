import neo4j.graph


class NodeD:
    def __init__(self, labels, properties):
        self.labels = labels
        self.properties = properties

    def to_json(self):
        return self.__dict__

    def __str__(self):
        return str(self.to_json())


class RelationshipD:
    def __init__(self, type, properties, node1: 'NodeD', node2: 'NodeD'):
        self.type = type
        self.properties = properties
        self.node1 = node1.to_json()
        self.node2 = node2.to_json()

    def to_json(self):
        return self.__dict__

    def __str__(self):
        return f'{self.node1} - {self.type} - {self.node2} ' + str(self.properties)


def transFormObject(obj):
    if isinstance(obj, neo4j.graph.Node):
        labels = list(obj.labels)
        properties = dict(obj)
        return NodeD(labels, properties)
    elif obj is not None:
        nodesR = [transFormObject(ls) for ls in obj.nodes]
        typeR = obj.type
        properties = dict(obj)
        return RelationshipD(typeR, properties, nodesR[0], nodesR[1])

    return obj



