#app/main/__init__.py
#https://stackoverflow.com/questions/68285731/app-route-and-template-render-not-working-in-flask

from flask import Blueprint

main = Blueprint('main', __name__, template_folder='templates', static_folder='static')
from . import routes 
# - Dieses Skript initialisiert ein Blueprint für das Hauptmodul der Webanwendung.
# - Konfiguration des Blueprints und Integration der Routen: ca. 5 Minuten