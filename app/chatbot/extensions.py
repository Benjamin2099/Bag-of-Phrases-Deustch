#app/chatbot/extensions.py

import torch
from pymongo import MongoClient
import os
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta

# Funktion zur Initialisierung des Torch-Geräts (CPU oder GPU)
def init_device():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    return device

client = MongoClient(os.getenv('MONGO_URI'))  # Verbindet sich mit der MongoDB-Instanz (MONGO_URI in .env-Datei)
db = client['Flask-app']  # Datenbank "Flask-app" wählen
interactions_collection = db['user_interactions']  # Sammlung für Benutzerinteraktionen

# Funktion zum Löschen alter Daten (älter als vier Wochen)
def delete_old_data():### Berechne das Datum von vor vier Wochen
    four_weeks_ago = datetime.now() - timedelta(weeks=4)  
    # Lösche Einträge, die älter als vier Wochen sind
    result = interactions_collection.delete_many({'timestamp': {'$lt': four_weeks_ago}})  
# Ausgabe der Anzahl gelöschter Einträge
    print(f'{result.deleted_count} alte Einträge wurden gelöscht')  

# Scheduler einrichten
scheduler = BackgroundScheduler()
scheduler.add_job(func=delete_old_data, trigger="interval", days=1)  # Führt die Bereinigung täglich durch
scheduler.start()

# Scheduler sauber beenden beim App-Shutdown
import atexit
atexit.register(lambda: scheduler.shutdown())  # Stoppt den Scheduler beim Beenden der Anwendung

#Zeit für Setup und Kommentierung: ca. 1.1 Stunde.

