
# tests/chatbot/test_routes.py
# Import die notwendigen Module und Funktionen für das Testen der Chatbot-Routen.
#https://stackoverflow.com/questions/4319825/python-unittest-opposite-of-assertraises
import unittest
from unittest.mock import patch, MagicMock
from flask_testing import TestCase
from flask import Flask
from app.chatbot.routes import chatbot_bp  # Absoluter Import
import torch

# Testklasse für die Chatbot-Routen
class TestChatbotRoutes(TestCase):
    def create_app(self):
        """
        Erstellen und Konfigurieren der Flask-App für Tests.
        """
        app = Flask(__name__)
        app.config['TESTING'] = True  # Aktivieren des Testmodus
        app.register_blueprint(chatbot_bp, url_prefix='/chatbot')  # Registrieren des Blueprints
        return app

    def setUp(self):
        """
        SetUp-Methode, die vor jedem Test ausgeführt wird.
        Initialisiert globale Variablen und bereitet die Testumgebung vor.
        """
        # Initialisieren von session_flags als leeres Dictionary für Tests
        global session_flags
        session_flags = {}
        super().setUp()  # Aufruf der Elternklasse SetUp-Methode

    @patch('app.chatbot.routes.init_device')  # Mock für init_device
    @patch('app.chatbot.routes.load_intents')  # Mock für load_intents
    @patch('torch.load')  # Mock für torch.load
    def test_model_load_failure(self, mock_torch_load, mock_load_intents, mock_init_device):
        """
        Test für das Scheitern des Modell-Ladens.
        Simuliert einen FileNotFoundError beim Laden des Modells.
        """
        # Simulieren, dass torch.load eine FileNotFoundError auslöst
        mock_torch_load.side_effect = FileNotFoundError("Modelldatei nicht gefunden")
        # Versuch, das Modell zu laden, sollte die Exception auslösen
        with self.assertRaises(FileNotFoundError) as context:
            torch.load('model.pth')  # Dies wird durch den Mock ersetzt

        # Überprüfen, ob die Fehlermeldung korrekt ist
        self.assertEqual(str(context.exception), "Modelldatei nicht gefunden")

    @patch('app.chatbot.routes.load_intents')  # Mock für load_intents
    def test_intents_load_failure(self, mock_load_intents):
        """
        Test für den Fall, dass die Intents-Datei nicht gefunden wird.
        Simuliert einen FileNotFoundError beim Laden der Intents.
        """
        # Simulieren, dass load_intents eine FileNotFoundError auslöst
        mock_load_intents.side_effect = FileNotFoundError("Intents-Datei nicht gefunden")

        # Versuch, die Intents zu laden, sollte die Exception auslösen
        with self.assertRaises(FileNotFoundError) as context:
            load_intents = mock_load_intents()  # Dies wird durch den Mock ersetzt

        # Überprüfen, ob die Fehlermeldung korrekt ist
        self.assertEqual(str(context.exception), "Intents-Datei nicht gefunden")

    @patch('app.chatbot.routes.get_response')  # Mock für get_response
    @patch('app.chatbot.routes.interactions_collection')  # Mock für interactions_collection
    def test_chat_route_success(self, mock_interactions_collection, mock_get_response):
        """
        Testet den erfolgreichen Ablauf einer Anfrage an die Chatbot-Route.
        Mockt die Antwort des Chatbots, um sicherzustellen, dass die Anfrage korrekt verarbeitet wird.
        """
        # Simulierte Antwort des Chatbots
        mock_get_response.return_value = "Hallo, wie kann ich Ihnen helfen?"
        # Senden einer Beispiel-POST-Anfrage
        response = self.client.post('/chatbot/chat', json={'message': 'hello'})
        # Überprüfen, ob der Statuscode 200 ist
        self.assertEqual(response.status_code, 200)
        # Überprüfen, ob die Antwort des Chatbots korrekt ist
        self.assertEqual(response.json['response'], "Hallo, wie kann ich Ihnen helfen?")
        # Überprüfen, ob insert_one einmal aufgerufen wurde
        mock_interactions_collection.insert_one.assert_called_once()

    @patch('app.chatbot.routes.get_response')  # Mock für get_response
    @patch('app.chatbot.routes.interactions_collection')  # Mock für interactions_collection
    def test_chat_route_failure(self, mock_interactions_collection, mock_get_response):
        """
        Testet den Fall, wenn während der Antwortgenerierung ein Fehler auftritt.
        Simuliert einen unerwarteten Fehler und überprüft die Fehlerbehandlung.
        """
        # Simulieren, dass get_response eine Exception auslöst
        mock_get_response.side_effect = Exception("Unerwarteter Fehler")
        
        # Zuerst eine Anfrage senden, um die user_id in session_flags zu setzen
        initial_response = self.client.post('/chatbot/chat', json={'message': 'Hallo'})
        self.assertEqual(initial_response.status_code, 200)
        self.assertIn('response', initial_response.json)
        
        # Nun eine zweite Anfrage mit derselben user_id senden, um get_response zu triggern
        failure_response = self.client.post('/chatbot/chat', json={'message': 'Hallo'})
        
        # Überprüfen, ob der Statuscode 500 ist
        self.assertEqual(failure_response.status_code, 500)
        # Überprüfen, ob die Fehlermeldung korrekt zurückgegeben wird
        self.assertIn('Unerwarteter Fehler', failure_response.json['error'])
        # Optional: Überprüfen, ob insert_one nicht aufgerufen wurde, da die Anfrage fehlschlug
        mock_interactions_collection.insert_one.assert_called_once()  # Nur der erste Aufruf

    @patch('app.chatbot.routes.interactions_collection')  # Mock für interactions_collection
    def test_chat_route_no_data(self, mock_interactions_collection):
        """
        Testet den Fall, wenn keine Nachricht gesendet wird.
        Erwartet einen 400 Bad Request zurück.
        """
        # Senden einer POST-Anfrage ohne Nachricht
        response = self.client.post('/chatbot/chat', json={})
        # Überprüfen, ob der Statuscode 400 ist
        self.assertEqual(response.status_code, 400)
        # Überprüfen, ob die Fehlermeldung korrekt ist
        self.assertIn('Nachricht ist erforderlich', response.json['error'])
        # Überprüfen, ob insert_one nicht aufgerufen wurde
        mock_interactions_collection.insert_one.assert_not_called()

if __name__ == '__main__':
    unittest.main()  # Führt die Tests aus, wenn das Skript direkt ausgeführt wird

# Zeit für die Implementierung und Tests: ca. 2:36 Stunden
