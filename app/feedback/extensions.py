#app/feedback/extensions.py
from pymongo import MongoClient
import os
def init_feedback_db():  
    client = MongoClient('mongodb://localhost:27017/')
    db = client['Flask-app']
    return db['feedback']  # Zeitdauer 15 Minuten

def init_feedback_collection(): # Zeitdaue 10 Minuten
    db = init_feedback_db()
    return db['feedback']
# feedback_db: Initialisiert die Verbindung zur MongoDB-Datenbank und gibt die 'feedback' Sammlung zurück.
# feedback_collection: Greift auf die 'feedback' Sammlung in der spezifischen Datenbank zu, indem sie init_feedbavk_db aufruft.
# Gesamte Zeitdauer 25 Minuten
