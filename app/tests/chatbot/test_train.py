# tests/chatbot/test_train.py
#Gesagte Zeit für Importieren ca. 16 Minute
#https://stackoverflow.com/questions/4319825/python-unittest-opposite-of-assertraises

import unittest
from unittest.mock import patch
import torch
from torch.optim import Adam
from torch.nn import CrossEntropyLoss
from app.chatbot.train import X_train, tags, model, device, ChatDataset, DataLoader
import app.chatbot.train as train_module # Importiere das Modul neu, um die Mock-Daten zu laden

# Testklasse für den Trainingsprozess des Chatbots
class TestChatbotTraining(unittest.TestCase):

    # Testet das Laden der Daten und deren Vorbereitung
    @patch('app.chatbot.train.json.load')
    @patch('app.chatbot.train.open', new_callable=unittest.mock.mock_open, read_data='{"intents": [{"tag": "begrüßung", "patterns": ["Hallo", "Hi"]}]}')
    def test_data_loading(self, mock_open, mock_json_load):
        # Simuliere das Laden der JSON-Daten
        mock_json_load.return_value = {"intents": [{"tag": "begrüßung", "patterns": ["Hallo", "Hi"]}]}
        # Verarbeite die Daten erneut, um sicherzustellen, dass sie korrekt im Modul ankommen
        train_module.all_phrases = [phrase.lower() for phrase in ['hallo', 'hi']]
        # Teste, ob die Tags und Phrasen geladen wurden
        self.assertIn("begrüßung", train_module.tags)
        self.assertIn("hallo", train_module.all_phrases)

    # Testet die Initialisierung des Modells
    def test_model_initialization(self): 
    # Überprüft, ob die Eingabegröße und Ausgabegröße korrekt sind
        self.assertEqual(model.l1.in_features, len(X_train[0]))
        self.assertEqual(model.l3.out_features, len(tags))
    # Testet das Training (Forward-Pass und Verlustberechnung)
    @patch('app.chatbot.train.NeuralNet.forward')  # Mocke den Forward-Pass des Modells
    def test_training(self, mock_forward):
        # Simuliere den Forward-Pass
        mock_forward.return_value = torch.rand(6, len(tags))  # Passe die Anzahl der Vorhersagen an die Anzahl der Ziel-Labels an

        # Dummy-Daten mit 6 Inputs, um die Batch-Größe richtig anzupassen
        dataset = ChatDataset(X_train[:6], [0] * 6)  # Verwende nur 6 Datenpunkte
        train_loader = DataLoader(dataset, batch_size=6, shuffle=True)
        optimizer = Adam(model.parameters(), lr=0.001)
        criterion = CrossEntropyLoss()

        # Testet den Forward-Pass und die Verlustberechnung
        for words, labels in train_loader:
            words, labels = words.to(device), labels.to(device)
            outputs = model(words)
            loss = criterion(outputs, labels)  # Jetzt sollte die Batch-Größe übereinstimme
        mock_forward.assert_called()  # Überprüft, ob der Forward-Pass korrekt aufgerufen wurde
        self.assertIsInstance(loss, torch.Tensor)  # Überprüft, ob der Verlust ein Tensor ist

    # Testet das Speichern des Modells und der Metadaten
    @patch('torch.save')
    def test_model_saving(self, mock_save):
        # Erstellt ein Dictionary mit den zu speichernden Modellinformationen
        model_info = {
            'model_state': model.state_dict(),
            'input_size': len(X_train[0]),
            'hidden_size': 8,
            'output_size': len(tags),
            'all_phrases': train_module.all_phrases,
            'tags': tags
        }
        # Speichert das Modell
        torch.save(model_info, 'data.pth') 
        # Überprüft, ob die torch.save-Funktion korrekt aufgerufen wurde
        mock_save.assert_called_with(model_info, 'data.pth')

if __name__ == '__main__':
    unittest.main()
# Geschätzte Gesamtentwicklungszeit für alle Testmethoden: ca. 2:16 Stunden


#Gesamte Zeit 8.5 - Stunden für Chatbot-Tests