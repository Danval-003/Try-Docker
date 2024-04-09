import os
from flask import Flask
from gridfs import GridFS
from neo4j import GraphDatabase
from dotenv import load_dotenv
from flask import jsonify
from pymongo import MongoClient
# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)
app.config['NEO4J_URI'] = os.getenv('NEO4J_URI')
app.config['NEO4J_USER'] = os.getenv('NEO4J_USERNAME')
app.config['NEO4J_PASSWORD'] = os.getenv('NEO4J_PASSWORD')
app.config['MONGO_URI'] = os.getenv('MONGO_URI')


neo4j_driver = GraphDatabase.driver(app.config['NEO4J_URI'],
                                    auth=(app.config['NEO4J_USER'], app.config['NEO4J_PASSWORD']))
mongo_client = MongoClient(app.config['MONGO_URI'])
db = mongo_client['social_network']
grid_fs = GridFS(db)
