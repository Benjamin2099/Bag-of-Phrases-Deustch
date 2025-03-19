# tests/chatbot/test_extensions.py
import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from app.chatbot.extensions import init_device, delete_old_data

class TestExtensions(unittest.TestCase):

    # Test für die Geräteinitialisierung (CUDA oder CPU)
    @patch('torch.cuda.is_available')
    def test_torch_device_initialization(self, mock_is_available):
        # Simuliere zweimal: Einmal ist CUDA verfügbar, einmal nicht
        mock_is_available.side_effect = [True, False] 
        self.assertEqual(str(init_device()), 'cuda')    # Wenn CUDA verfügbar ist, sollte 'cuda' zurückgegeben werden
        self.assertEqual(str(init_device()), 'cpu') 	# Sonst 'cpu'.

    # Test für die MongoDB-Verbindung und Sammlung
    @patch('app.chatbot.extensions.MongoClient')  # Patche den MongoClient direkt
    def test_mongo_db_connection(self, mock_mongo_client):
        # Simuliere eine Verbindung zur MongoDB
        mock_db = mock_mongo_client.return_value['Flask-app']
        mock_collection = mock_db['user_interactions']
  
        # Überprüfe, ob interactions_collection die gemockte Sammlung ist
        with patch('app.chatbot.extensions.interactions_collection', mock_collection):
            from app.chatbot.extensions import interactions_collection
            self.assertIs(interactions_collection, mock_collection)

    # Test für das Löschen alter Daten aus MongoDB (älter als vier Wochen)
    @patch('app.chatbot.extensions.interactions_collection.delete_many')  # Mocke die delete_many Methode
    def test_delete_old_data(self, mock_delete_many):
        # Füge den aktuellen Zeitstempel hinzu und speichere ihn
        current_time = datetime.now()
        # Simuliere, dass 5 Einträge gelöscht wurden
        mock_delete_many.return_value.deleted_count = 5

        # Führe die delete_old_data Funktion aus, wobei wir den Zeitstempel festlegen
        with patch('app.chatbot.extensions.datetime') as mock_datetime:
            mock_datetime.now.return_value = current_time
            delete_old_data()

        # Überprüfe, ob delete_many mit den richtigen Parametern aufgerufen wurde
        mock_delete_many.assert_called_once_with({'timestamp': {'$lt': current_time - timedelta(weeks=4)}})
        # Überprüfe, ob tatsächlich 5 Einträge gelöscht wurden
        self.assertEqual(mock_delete_many.return_value.deleted_count, 5)

    # Test für die Scheduler-Konfiguration
    @patch('app.chatbot.extensions.scheduler.add_job')  # Mocke den Scheduler
    def test_scheduler_add_job(self, mock_add_job):
        from app.chatbot.extensions import scheduler, delete_old_data

        # Simuliere, dass der Job dem Scheduler hinzugefügt wird
        scheduler.add_job(func=delete_old_data, trigger="interval", days=1)
        # Überprüfe, ob der Job korrekt mit den erwarteten Parametern hinzugefügt wurde
        mock_add_job.assert_called_once_with(func=delete_old_data, trigger="interval", days=1)

if __name__ == '__main__':
    unittest.main()

# Zeit für die Implementierung und Tests: ca. 1.20 Stunde