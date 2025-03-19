#config.py

import os
from dotenv import load_dotenv
#https://flask.palletsprojects.com/en/3.0.x/quickstart/#debug-mode
load_dotenv()  # Lädt die Umgebungsvariablen aus der .env-Datei  

class Config:
    #Konfigurationsklasse aus Umgebungsvariablen lädt. # Zeitdauer: 25 Minuten
    SECRET_KEY = os.environ.get('SECRET_KEY')  #  geheimen Schlüssel
    MONGO_URI = os.environ.get('MONGO_URI')  # Lädt die MongoDB URI
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")  #JWT geheimen Schlüssel (Json Web Token)
    MODEL_PATH = os.environ.get('MODEL_PATH')  # Pfad zum Modell.pytorch 
    INTENTS_PATH = os.environ.get('INTENTS_PATH')  # Pfad zu den Intents.json
    DEV_MONGO_URI=os.environ.get('DEVELOPMENT_MONGO_URI')  # Entwicklungs - mongoDB URI
    PROD_MONGO_URI=os.environ.get('PRODUCTION_MONGO_URI')  # Produktions - mongoDB URI

class DevelopmentConfig(Config):
    #Entwicklungskonfigurationen # Zeitdauer: 5 Minuten
    DEBUG = True  # Aktiviert den Debug-Mdus
    FLASK_ENV = 'development'  # Setzt die Flask-Umgebung auf 'development' 
    MONGO_URI = os.environ.get('DEV_MONGO_URI', Config.MONGO_URI)  # Alternative URI für die Entwicklung

class ProductionConfig(Config):
    #Produktionskonfig #Zeitdauer: 5 Minuten
    DEBUG = False  # Deaktiviert den Debug-Modus
    FLASK_ENV = 'production'  
    MONGO_URI = os.environ.get('PROD_MONGO_URI', Config.MONGO_URI)  # Produktions-MongoDB URI

class TestingConfig(Config):
    #Testkonfig #Zeitdauer: 10 Minuten
    TESTING = True  # Aktiviert den Testmodus
    DEBUG = True # Aktviert den Debug-Modus 
    MONGO_URI = os.environ.get('TEST_MONGO_URI')  # Test- mongoDB URI
    WTF_CSRF_ENABLED = False  # Deaktiviert CSRF-Schutz für Testing

# Gesamtdauer für die Bearbeitung Config - 45 - Minute und .env: - 25 - Minute
# Gesamtdauer 1:10 Stunde

