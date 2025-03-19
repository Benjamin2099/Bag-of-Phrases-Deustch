 
# tests/chatbot/test_model.py

import torch #Importiert PyTorch-Bibliothek für das Training und Testen 
from app.chatbot.model import NeuralNet# Importiert die NeuralNet-Klasse aus modl.py
import unittest #Unittest-Bibliothek für das Schreiben und Ausführen von Tests.

class TestNeuralNet(unittest.TestCase): #Definiert eine Testklasse, die von unittest.TestCase erbt.
    def test_forward_pass(self):
        input_size = 10  #Setzt die Parameter für das neuronale Netzwerk.
        hidden_size = 20
        num_classes = 3
        model = NeuralNet(input_size, hidden_size, num_classes) # Erstellt eine Instanz des neuronalen Netzwerks.
        sample_input = torch.randn(1, input_size) #Generiert eine zufällige Eingabe für den Test.
        output = model(sample_input)# Führt das Model mit der Eingabe durch und erzeugt eine Ausgabe
        self.assertEqual(output.shape, (1, num_classes)) # überprüft, dass die Ausgabe die erwartete Form hat.

if __name__ == '__main__':
    unittest.main()

# Zeit für die Implementierung und Tests: ca. 45 Minuten Stunde