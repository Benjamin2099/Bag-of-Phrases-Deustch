# Importieren des Blueprint-Moduls aus dem Flask-Paket
from flask import Blueprint

# Blueprint-Initialisierung und Import von Routen 
feedback_bp = Blueprint('feedback', __name__, template_folder='templates', static_folder='static')

from . import routes
# Importieren der Routing-Funktionen aus der routes.py innerhalb des feedback-Moduls

# Einrichtung und Test der Routenintegration: 5 Minuten
