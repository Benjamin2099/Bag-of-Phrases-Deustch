#app/__init__.py
#https://docs.python.org/3/tutorial/index.html
#https://flask.palletsprojects.com/en/3.0.x/
#https://stackoverflow.com/
#https://stackoverflow.com/questions/49915758/what-is-flask-route
#https://flask.palletsprojects.com/en/3.0.x/quickstart/#rendering-templates
#https://flask.palletsprojects.com/en/3.0.x/quickstart/#logging
# app/__init__.py
from flask import Flask, abort, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
import os

# Initialisierung der Erweiterungen (außer Flask)
mongo = PyMongo()
limiter = Limiter(key_func=get_remote_address, default_limits=["180 per day", "50 per hour"])
talisman = Talisman()

def create_app(config_name=None):
    app = Flask(__name__)
    
    # Laden der Umgebungsvariablen aus der .env-Datei
    load_dotenv()

    # Lesen des Konfigurationspfads aus der .env-Datei und Hinzufügen zum Python-Pfad
    config_path = os.getenv('CONFIG_PATH')
    if config_path is None or not os.path.isfile(config_path):
        raise Exception(f"Config file not found or CONFIG_PATH not set: {config_path}")

    config_dir = os.path.dirname(config_path)
    os.sys.path.append(config_dir)

    # Importieren der Konfihurationsklassen
    from config import Config, DevelopmentConfig, ProductionConfig, TestingConfig
    # Auswahl der entsprechenden Konfigurationsklasse
    config_classes = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig
    }
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    app.config['CONFIG_NAME'] = config_name  # Setzen der Config-Name in die App-Konfiguration
    config_class = config_classes.get(config_name, Config)
    app.config.from_object(config_class)  # Anwenden der ausgewählten Konfiguration

    # Initialisierung der Erweiterungen mit der App
    try:
        mongo.init_app(app)  # Initialisierung von MongoDB
        app.logger.info("MongoDB initialized successfully")
    except Exception as e:
        app.logger.error(f"MongoDB initialization failed: {e}")
        raise e  # Fehler erneut werfen, um mehr Informationen zu erhalten
    limiter.init_app(app)  # Initialisierung der Ratenbegrenzung

    # Initialisierung von Flask-talisman für Sicherheitsheader und HTTPS-Erzwingung
    if config_name != 'development':
        talisman.init_app(app, content_security_policy={
            'default-src': [
                '\'self\'',
                'https://stackpath.bootstrapcdn.com',
                'https://code.jquery.com',
                'https://cdn.jsdelivr.net',
                'https://www.dropbox.com'
            ],
            'img-src': [
                '\'self\'',
                'https://www.dropbox.com',
                '*'  
            ],
            'style-src': [
                '\'self\'',
                'https://stackpath.bootstrapcdn.com',
                'https://cdn.jsdelivr.net'
            ],
            'script-src': [
                '\'self\'',
                'https://code.jquery.com',
                'https://cdn.jsdelivr.net'
            ],
            'connect-src': [
                '\'self\'',
                'http://localhost:5000',
                'http://127.0.0.1:5000',
                'https://innotech-experts.de/'
            ]
        })
    else:
        talisman.init_app(app, content_security_policy=None)  # Keine CSP in der Entwicklung

    # Initiallisierung von CORS
    allowed_origins = os.getenv('ALLOWED_ORIGINS', 'http://localhost:5000,http://127.0.0.1:5000,https://innotech-experts.de/').split(',')
    allowed_origins = [origin.strip() for origin in allowed_origins]  # Entfernt Leerzeichen
    CORS(app, resources={
        r"/feedback/*": {"origins": allowed_origins},
        r"/chatbot/*": {"origins": allowed_origins},
        r"/api/*": {"origins": allowed_origins}  # Falls verwendet
    })

    setup_logging(app)        # Einrichten des Loggings
    # Registrieren von Blueprints
    from app.feedback.routes import feedback_bp
    app.register_blueprint(feedback_bp, url_prefix='/feedback')
    from app.chatbot.routes import chatbot_bp
    app.register_blueprint(chatbot_bp, url_prefix='/chatbot')
    from app.main.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    register_error_handlers(app)  # Globale Fehlerhandler registrieren
    # Sichere Sitzungsverwaltung
    app.config.update(
        SESSION_COOKIE_SECURE=True,      # Nur über HTTPS senden
        SESSION_COOKIE_HTTPONLY=True,    # Nicht über JavaScript zugänglich
        SESSION_COOKIE_SAMESITE='Lax'    # Einschränkung von Cross-Site-Requests
    )

    # Entfernen Sie die eigene HTTPS-Middleware, da Flask-Talisman dies bereits übernimmt
    return app

def setup_logging(app):
    log_dir = 'app/logs'  # Stelle sicher, dass das Verzeichnis für die Log-Dateien existiert.
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    # Konfiguriere Logging, um alle Requests und Anwendungsereignisse zu erfassen.
    file_handler = RotatingFileHandler(os.path.join(log_dir, 'application.log'), maxBytes=1024000, backupCount=5)
    log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # Logge alle HTTP-Anfragen
    file_handler.setFormatter(log_format)
    file_handler.name = 'werkzeug'  # Setze den Namen des Handlers explizit
    app.logger.addHandler(file_handler)  # Füge den Handler zum App-Logger und zum werkzeug.
    logging.getLogger('werkzeug').addHandler(file_handler)
    app.logger.setLevel(logging.INFO)  # Setze das Logging-Level
    logging.getLogger('werkzeug').setLevel(logging.INFO)

def register_error_handlers(app):
    from flask import jsonify
    from werkzeug.exceptions import HTTPException

    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        response = e.get_response()
        response.data = jsonify({
            "error": e.name,
            "description": e.description,
        }).data
        response.content_type = "application/json"
        return response

    @app.errorhandler(Exception)
    def handle_exception(e):
        app.logger.error(f"Unehandelter Fehler: {e}", exc_info=True)
        return jsonify({"error": "Interner Serverfehler"}), 500

# Entwicklungszeit:------------------------------------------>
# Grundsetup und Importe: 40 minute.
# Einrichtung der Konfigurationen und Erweiterungen: 45Mnuten.
# Registrierung der Blueprints und Logging: 25 Minute.
# Geschätzte Gesamtdauer: ca. 1:50 Stunden.
#Flask-Doku: https://flask.palletsprojects.com/
#Flask-CORS Doku: https://flask-cors.readthedocs.io/
#Flask-Limiter Doku: https://flask-limiter.readthedocs.io/
#Flask-Talisman Doku: https://github.com/GoogleCloudPlatform/flask-talisman
#Postman: https://www.postman.com/ – Zum Testen von API-Endpunkten.
"""
Entwicklung: Aktiviert typischerweise Debugging, detaillierte Fehlermeldungen und automatisches Neuladen.

Produktion: Optimiert die Leistung und das Logging, deaktiviert Debug-Funktionen.

Testen: Wird üblicherweise verwendet, um eine Testumgebung mit Testdatenbanken, Simulation externer Dienste usw. einzurichten
"""

