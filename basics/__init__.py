import os
from flask import Flask
from neo4j import GraphDatabase
from dotenv import load_dotenv
from flask import jsonify

# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)
app.config['NEO4J_URI'] = os.getenv('NEO4J_URI')
app.config['NEO4J_USER'] = os.getenv('NEO4J_USERNAME')
app.config['NEO4J_PASSWORD'] = os.getenv('NEO4J_PASSWORD')

neo4j_driver = GraphDatabase.driver(app.config['NEO4J_URI'],
                                    auth=(app.config['NEO4J_USER'], app.config['NEO4J_PASSWORD']))