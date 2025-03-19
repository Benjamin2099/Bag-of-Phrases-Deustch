#app/chatbot/model.py

# Definition des NeuralNet, das von nn.Module erbt
import torch.nn as nn
#https://pytorch.org/docs/stable/nn.html
#https://pytorch.org/docs/stable/nn.functional.html
#https://pytorch.org/docs/stable/index.html
class NeuralNet(nn.Module): 
    def __init__(self, input_size, hidden_size, num_classes):
        super(NeuralNet, self).__init__()
         # Definiere drei lineare Schichten und eine ReLU-Aktivierungsfunktion
        self.l1 = nn.Linear(input_size, hidden_size)  # Erste Schicht vom Eingabe- zum versteckten Layer
        self.l2 = nn.Linear(hidden_size, hidden_size)  # Zweite versteckte Schicht
        self.l3 = nn.Linear(hidden_size, num_classes)  # Ausgabeschicht vom letzten versteckten Layer zur Anzahl der Klassen
        self.relu = nn.ReLU()  # ReLU-Aktivierungsfunktion

    def forward(self, x):
        # Define the forward pass
        x = self.relu(self.l1(x))  # Wendet ReLU auf die Ausgabe der ersten Schicht an
        x = self.relu(self.l2(x))  # ##### der zweiten Schicht an
        x = self.l3(x)  # Ausgabeschicht hat kein ReLU, da es typischerweise mit einer Verlustfunktion verwendet wird, die Softmax beinhaltet
        return x

# NeuralNet-Klasse definiert ein neuronales Netzwerk mit drei Linear-Layern und ReLU als Aktivierungsfunktion.
# Eingabegröße, Anzahl die versteckten Neuronen und Klassenanzahl sind konfigurierbar.
#Die 'forward' Methode definirt den Durchlauf eines Inputs durch das Netz, mit Aktivierung nach den ersten beiden Layern.
# Zeit für die Implementierung und Kommentierung: ca. 46 Minuten.
