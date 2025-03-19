#app/chatbot/__init__.py
from flask import Blueprint

# Blueprint-Initialisierung und Import von Routen 
chatbot_bp = Blueprint('chatbot', __name__, template_folder='templates', static_folder='static')

from . import routes

# - Blueprint für das Chatbot-Modul wird hier initialisiert.
# - Zeit für Einrichtung und Kommentierung: ca. 15 Minuten.

#https://pytorch.org/docs/stable/index.html
#https://stackoverflow.com/
#https://pytorch.org/docs/stable/index.html