from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import pymysql
from flask_restx import Api, Resource
from flask import json
from datetime import datetime
from sqlalchemy import inspect
from functools import wraps
from flask import redirect, url_for, session

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/cesi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def custom_json_encoder(o):
    if isinstance(o, datetime):
        return o.isoformat()
    raise TypeError("Type not serializable")

app.json_encoder = custom_json_encoder

app.secret_key = 'cesi_di_2023'

db_params = {
            'host': 'localhost',
            'user': 'root',
            'password': '',
            'db': 'cesi',
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor
        }

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    @staticmethod
    def create_table_if_not_exists():
        inspector = inspect(db.engine)
        if not inspector.has_table('user'):
            db.create_all()


class Temperature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Date = db.Column(db.DateTime, default=db.func.current_timestamp())
    Temperature = db.Column(db.Float, nullable=False)
    Humidite = db.Column(db.Float, nullable=False)

    @staticmethod
    def create_table_if_not_exists():
        inspector = inspect(db.engine)
        if not inspector.has_table('temperature'):
            db.create_all()

@api.route('/api/temperature')
class TemperatureResource(Resource):
    def get(self):

        connection = pymysql.connect(**db_params)
        try:
            with connection.cursor() as cursor:
                sql = "SELECT `Date`, `Temperature`, `Humidite` FROM `temperature` ORDER BY `Date` DESC "
                cursor.execute(sql)
                rows = cursor.fetchall()

                data = [
                    {
                        'Date': row['Date'].isoformat() if isinstance(row['Date'], datetime) else row['Date'],
                        'Temperature': row['Temperature'],
                        'Humidite': row['Humidite']
                    }
                    for row in rows
                ]
                return data
        finally:
            connection.close()
    def post(self):
        data = api.payload

@api.route('/api/temperature/share')
class TemperatureResource(Resource):
    def get(self):
        
        connection = pymysql.connect(**db_params)
        try:
            with connection.cursor() as cursor:
                sql = "SELECT `Date`, `Temperature`, `Humidite` FROM `temperature` ORDER BY `Date` DESC LIMIT 1"
                cursor.execute(sql)
                rows = cursor.fetchall()

                data = [
                    {
                        'Date': row['Date'].isoformat() if isinstance(row['Date'], datetime) else row['Date'],
                        'Temperature': row['Temperature'],
                        'Humidite': row['Humidite']
                    }
                    for row in rows
                ]
                return data
        finally:
            connection.close()

        connection = pymysql.connect(**db_params)
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO temperature (Temperature, Humidite) VALUES (%s, %s)"
                cursor.execute(sql, (data['Temperature'], data['Humidite']))
                connection.commit()
                return {"message": "Data inserted successfully"}, 201
        except Exception as e:
            return {"error": str(e)}, 500
        finally:
            connection.close()

@api.route('/api/temperature/recent')
class RecentTemperatureResource(Resource):
    def get(self):
        connection = pymysql.connect(**db_params)
        try:
            with connection.cursor() as cursor:
                sql = "SELECT `Date`, `Temperature`, `Humidite` FROM `temperature` ORDER BY `Date` DESC LIMIT 5"
                cursor.execute(sql)
                rows = cursor.fetchall()
                data = [
                    {
                        'Date': row['Date'].isoformat() if isinstance(row['Date'], datetime) else row['Date'],
                        'Temperature': row['Temperature'],
                        'Humidite': row['Humidite']
                    }
                    for row in rows
                ]
                return data
        finally:
            connection.close()

@api.route('/api/temperature/today')
class RecentTemperatureResource(Resource):
    def get(self):
        connection = pymysql.connect(**db_params)
        try:
            with connection.cursor() as cursor:
                sql = "SELECT `Date`, `Temperature`, `Humidite` FROM `temperature` WHERE DATE(Date) = CURDATE() "
                cursor.execute(sql)
                rows = cursor.fetchall()
                data = [
                    {
                        'Date': row['Date'].isoformat() if isinstance(row['Date'], datetime) else row['Date'],
                        'Temperature': row['Temperature'],
                        'Humidite': row['Humidite']
                    }
                    for row in rows
                ]
                return data
        finally:
            connection.close()

@api.route('/api/temperature/lastday')
class RecentTemperatureResource(Resource):
    def get(self):
        connection = pymysql.connect(**db_params)
        try:
            with connection.cursor() as cursor:
                sql = "SELECT `Date`, `Temperature`, `Humidite` FROM `temperature` WHERE Date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY) "
                cursor.execute(sql)
                rows = cursor.fetchall()
                data = [
                    {
                        'Date': row['Date'].isoformat() if isinstance(row['Date'], datetime) else row['Date'],
                        'Temperature': row['Temperature'],
                        'Humidite': row['Humidite']
                    }
                    for row in rows
                ]
                return data
        finally:
            connection.close()

@app.route('/temperature')
@login_required
def temperature():
    return render_template('temperature.html')

@app.route('/graphique')
@login_required
def graphique():
    return render_template('graphique.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['username'] = user.username
            return redirect(url_for('temperature'))
        else:
            redirect(url_for('login'))

    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(username=username,email=email, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')

if __name__ == '__main__':
    with app.app_context():
        User.create_table_if_not_exists()
        Temperature.create_table_if_not_exists()

    app.run(debug=True)
