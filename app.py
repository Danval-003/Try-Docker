from basics import app, neo4j_driver, jsonify
from tools import *
from routes import create, delete
import os
import warnings
from gridfs_routes import gridR

app.register_blueprint(create)
app.register_blueprint(delete)
app.register_blueprint(gridR)


@app.route('/api/nodos')
def obtener_nodos():
    records = makeQuery()
    warnings.warn('This is a warning')
    return convertJson(records)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!' + str(os.getenv('NEO4J_URI'))


if __name__ == '__main__':
    app.run(host='0.0.0.0')
