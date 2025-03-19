#app/main/routes.py
from flask import Blueprint, render_template
# Rendert HTML-Seiten
# request für Zugriff auf Nutzerdaten aus HTTP-Anfragen.
# flash Zeigt temporäre Benachrichtigungen an.

# Definiere ein Blueprint für das Hauptmodul der Anwendung
main = Blueprint('main', __name__)

@main.route('/')
def home():
    """ Zeige die Startseite mit einem Suchformular für Jobs. """
    return render_template('base.html')# Rendert die Startseite mit dem Suchformular 

# Gesamtdauer der Entwicklung: 20 Minuten
# Gesamtdauer für main: 25 Minuten
#https://flask.palletsprojects.com/en/3.0.x/quickstart/#routing
#https://flask.palletsprojects.com/en/3.0.x/tutorial/templates/


# Gesamtdauer der Entwicklung: 20 Minuten
# Gesamtdauer für main: 25 Minuten
#https://flask.palletsprojects.com/en/3.0.x/quickstart/#routing
#https://flask.palletsprojects.com/en/3.0.x/tutorial/templates/