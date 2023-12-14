# # -*- coding: utf-8 -*-
from encodings import utf_8
from fileinput import filename
#import mysql.connector
import json
from doctest import debug
from flask import Flask, render_template, request, jsonify, url_for
from flask_restplus import Api, Resource, fields
import pymysql




app = Flask(__name__)#, template_folder='templates')
api = Api(app, version='1.0', title='Mon Api', description='API pour recuperer des donnees depuis MariaDB')

# Configuration de la base de donnees
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "azerty",
    "database": "stationmeteo"
}

# Classe de gestion des requêtes HTTP

@app.route('/do_POST', methods=['POST'])        
def handle_post():

    content_length = int(request.headers['Content-Length'])
    post_data = request.data
    print(post_data)
    data = json.loads(post_data.decode('utf-8'))
        
    # Extraction des données
    temperature = data.get('temperature')
    humidite = data.get('humidite')
        
    if temperature is not None and humidite is not None:
        # Connexion à la base de données
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Insertion des données dans la base de données
        insert_query = "INSERT INTO relevemeteo (Temperature, Humidite) VALUES (%s, %s)"
        cursor.execute(insert_query, (temperature, humidite))
        conn.commit()
            
        cursor.close()
        conn.close()

        return jsonify({'message' : 'Donnees enregistrees'})
    else:
       return jsonify({'error': 'Donnees incompletes'})
    
    
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='azerty',
    database='stationmeteo'
)
cursor = conn.cursor()
@app.route('/meteo')
def index():
        cursor.execute('SELECT Temperature, Humidite, Date FROM relevemeteo WHERE IdTemperature between 70 AND 80')
        result = cursor.fetchall()
        data_temperature = [(row[2].strftime("%d/%m/%Y %H:%M:%S"), row[0]) for row in result]
        data_humidite = [(row[2].strftime("%d/%m/%Y %H:%M:%S"), row[1]) for row in result]
        
        labels_temperature = [row[0] for row in data_temperature]
        values_temperature = [row[1] for row in data_temperature]
        
        labels_humidite = [row[0] for row in data_humidite]
        values_humidite = [row[1] for row in data_humidite]
        
        return render_template('Meteo.html', labels_temperature=labels_temperature, values_temperature=values_temperature, labels_humidite=labels_humidite, values_humidite=values_humidite)

modele_donnees = api.model('Donnees', {
    'temperature': fields.Float(required=True, description='La temperature actuel'),
    'humidite': fields.Float(required=True, description='humidite actuel')
    })

@api.route('/donnees')
class DonneesResource(Resource):
    @api.marshal_with(modele_donnees)
    def get(self):    
        
        cursor.execute('SELECT Temperature, Humidite, Date FROM relevemeteo WHERE IdTemperature BETWEEN 1 AND 10')
        result = cursor.fetchall()
        print(result)
        
        donnees = [{'temperature': row[0], 'humidite': row[1]} for row in result]
        return donnees

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
    print('Serveur HTTP demarre sur le port 5000...')



