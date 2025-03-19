#app/chatbot/routes.py

import os
import random
from flask import Blueprint, request, jsonify
import torch
from app.chatbot.model import NeuralNet
from app.chatbot.nltk import tokenize_to_ngrams, bag_of_phrases
import json
from dotenv import load_dotenv
from app.chatbot.extensions import init_device, interactions_collection
from datetime import datetime
ch_bp = Blueprint('feedback', __name__)
# Datenschutzrichtlinie definieren
PRIVACY_NOTICE = """
Herzlich willkommen! Bitte akzeptieren Sie unsere Datenschutzbestimmungen, 
um die Unterhaltung mit dem Chatbot fortzusetzen. 
Ihre Daten werden ausschließlich zur Verbesserung des Chatbots verwendet und gemäß den geltenden Datenschutzvorgaben verarbeitet. 
Vielen Dank für Ihr Verständnis!“
"""


# Flag zur Nachverfolgung der ersten Interaktion
session_flags = {}
# Lade Umgebungsvariablen aus der .env-Datei
load_dotenv()
# Pfade aus Umgebungsvariablen für das Modell und die Intents JSON holen
MODEL_PATH = os.getenv('MODEL_PATH')
INTENTS_PATH = os.getenv('INTENTS_PATH')

# Blueprint für den Chatbot-Teil der Flask-App einrichten
chatbot_bp = Blueprint('chatbot', __name__)
# Gerät für PyTorch initialisierem
device = init_device()

# Trainiertes Modell und Trainingsdaten laden
# Stellt sicher, dass das Modell auf das richtige Gerät geladen wird
model_data = torch.load(MODEL_PATH, map_location=device)
model = NeuralNet(model_data["input_size"], model_data["hidden_size"], model_data["output_size"]).to(device)
model.load_state_dict(model_data['model_state'])
model.eval()

# Wörter (Phrasen) und Tags aus dem Modell-Daten laden
all_phrases = model_data['all_phrases']  # Phrasen anstelle von Wörtern
tags = model_data['tags']

# Funktion, um die Intents zu laden
def load_intents():
    with open(INTENTS_PATH, 'r', encoding='utf-8') as file:
        intents = json.load(file)
    return intents

intents = load_intents()

""" Funktion zur Generierung einer Antwort. """
def get_response(msg):  # Nachricht in n-Gramme (Phrasen) zerlegen
    sentence = tokenize_to_ngrams(msg)  # Tokenisierung in n-Gramme
    # Erzeugen eines "Bag of Phrases" Vektors
    X = bag_of_phrases(sentence, all_phrases)  # Verwende Phrasen anstelle von Wörtern
    # Umwandeln in PyTorch Tensor und auf das richtige Gerät bringen.
    X = torch.from_numpy(X).reshape(1, X.shape[0]).to(device)
    output = model(X)  # Vorhersage durchführen
    _, predicted = torch.max(output, dim=1)  # Klassifikation bestimmen
    tag = tags[predicted.item()]  # Den Tag (Intent) der Vorherssage bekommen.
    probs = torch.softmax(output, dim=1)  # Wahrscheinlichkeiten durch Softmax ermitteln
    prob = probs[0][predicted.item()]  # Wahrscheinlichkeit für die vorhergesagte Klasse

    print("Tag:", tag, "Probability:", prob.item())  # Debug-output: Tag und Wahrscheinlichkeit
    # Prüfe die Wahrscheinlichkeit, um eine Antwort zu wählen
    if prob.item() > 0.25:  # Wenn die Wahrscheinlichkeit hoch genug ist.
        for intent in intents['intents']:  # Intents durchsuchen
            if tag == intent["tag"]:  # Richtigen Intent finden
                print("Found intent:", intent["tag"])  # Debug-output: Gefundener Intent
                return random.choice(intent['responses'])  # Zufällige Antwort auswählen
    return "Entschuldigung, das habe ich nicht verstanden. Könnten Sie bitte Ihre Frage etwas spezifischer formulieren?"
    
#API Endpoint
@chatbot_bp.route('/chat', methods=['POST'])
def chat():
    try:
        # Benutzer-ID oder Sitzungs-ID erhalten (optional)
        user_id = request.json.get('user_id', "unbekannt") 
        # Nachricht des Benutzers erhalten
        user_input = request.json.get('message')
        # Fehlerbehandlung, wenn keine Nachricht gesendet wurde
        if not user_input:
            return jsonify({'error': 'Nachricht ist erforderlich'}), 400
        # Überprüfen, ob es die erste Interaktion der Sitzung ist
        if user_id not in session_flags:
            session_flags[user_id] = True
            interactions_collection.insert_one({
                'user_id': user_id,
                'user_input': None,
                'bot_response': PRIVACY_NOTICE,
                'timestamp': datetime.now(),
                'is_first_interaction': True
            })
            return jsonify({'response': PRIVACY_NOTICE})
        # Erhalte die Antwort des Chatbots basierend auf der Benutzereingabe
        response = get_response(user_input)

        # Speichere die Interaktion in der MongoDB
        interactions_collection.insert_one({
            'user_id': user_id,
            'user_input': user_input,
            'bot_response': response,
            'timestamp': datetime.now(),
            'is_first_interaction': False
        })
        # Gib die Antwort als JSON zurück
        return jsonify({'response': response})
    except Exception as e:
        # Fehlerbehandlung, falls ein unerwarteter Fehler auftritt
        return jsonify({'error': str(e)}), 500

"""
Dieses Skript stellt einen Chatbot-Service bereit, der über eine Flask-Anwendung läuft.
Es lädt trainierte Modell- und Intent-Daten, setzt eine REST-API mit Flask auf und verarbeitet Anfragen, um auf Benutzereingaben zu antworten.
Das System verwendet ein trainiertes neuronales Netzwerk, um die Absichten des Benutzers zu erkennen und entsprechend zu reagieren.
"""
# Einrichtung des Flask-Blueprints und Routing: 15 Minuten
# Initialisierung und Laden des Modells: 30 Minuten
# API-Endpunkt zur Verarbeitung und Antwortgenerierung: 45 Minuten
# Integration der Datenbank für das Speichern von Interaktionen: 30 Minuten

# Gesamtdauer für das Implementieren dieses Scripts: 2 - Stunde

