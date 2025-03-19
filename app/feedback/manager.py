
from datetime import datetime # Import für Datum und Zeit
from pymongo import MongoClient

def init_feedback_collection(): 
    client = MongoClient('mongodb://localhost:27017/')
    db = client['Flask-app']
    return db['feedback'] # Zeitdauer: 10 Minuten

class FeedbackManager:
    def __init__(self):
        self.feedback_collection = init_feedback_collection() # Zeitdauer: 5 Minuten

    def save_feedback(self, feedback_data): 
        """Speichert Feedback-Daten in der Datenbank."""  
        feedback_document = {
            'rating': feedback_data.get('rating'),
            'name': feedback_data.get('name'),
            'email': feedback_data.get('email'),
            'feedback': feedback_data.get('feedback'),
            'gesendet_am': datetime.now()  # Speichern des aktuellen Datums und der Uhrzeit  # Datum und Uhrzeit speichern
        }
        self.feedback_collection.insert_one(feedback_document)
        return {'message': 'Danke für Ihr Feedback!'} # Zeitdauer: 20 Minuten

# init_feedback_collection:Initialisiert die Verbindung zur MongoDB-Datenbank und gibt die 'feedback' Sammlung zurück.
# FeedbackManager Klasse: Verwalter für Feedback-Operationen.
# __init__, Initialisiert die feedback_collection durch Aufruf von init_feedback_collection.
# save_feedback-Methode: Speichert Feedback-Daten in der feedback Sammlung.

# Gesamtdauer für die Bearbeitung: 35 Minuten
