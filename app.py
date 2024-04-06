from basics import app, neo4j_driver, jsonify
from tools import *
import os


@app.route('/api/nodos')
def obtener_nodos():
    print(os.getenv('NEO4J_URI'))
    records = makeQuery("""
Match(p:Person {name: 'Tom Cruise'})
MATCH(m:Movie)
MATCH(p) - [r] - (m)

return p, r, m
    """, listOffIndexes=['r', 'm'])
    return convertJson(records)



@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
