
#app/chatbot/train.py
#python train.py
#https://pytorch.org/docs/stable/nn.html
#https://fasttext.cc/docs/en/crawl-vectors.html
#https://keras.io/api/keras_nlp/tokenizers/
#Beim trainieren sollte die punkte vor diese module(nlp_utils,model,extensions) entfern werden 
#Beim testen sollte vor diese module(nlp_utils,model,extensions) eine Punkte entstehen.
#--------------------------------------------------------------------------------------------------------->
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import json
import os
import matplotlib.pyplot as plt  # Importiere matplotlib für die Diagrammerstellung
from .nltk import tokenize_to_ngrams, bag_of_phrases  # Wir importieren jetzt tokenize_to_ngrams
from .model import NeuralNet
from .extensions import init_device

# Gerätekonfiguration
device = init_device()
# Pfade für Dateizugriffe vorbereiten
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
file_path = os.path.join(base_dir, 'intents.json')  # Pfad zur Datei intents.json festlegen
# Daten aus intents.json laden
with open(file_path, 'r', encoding='utf-8') as file:  # Öffnet die intents.json
    intents = json.load(file)  # Lädt den Inhalt der Datei in ein Dictionary

all_phrases = []  # Liste zur Speicherung aller Phrasen (n-Gramme)
tags = []  # Liste aller Tags
xy = []  # Liste der Wort-Tag-Paare
# Daten vorbereiten-------------------------------------------------------------
for intent in intents['intents']:  # Iteriert über jede Absicht im intents.json
    tag = intent['tag']  # Extrahiert das Tag der aktuellen Absicht.
    tags.append(tag)  # Fügt das Tag zur Tags-Liste hinzu.
    for pattern in intent['patterns']:  # Iteriert über jedes Muster in der aktuellen Absicht
        phrases = tokenize_to_ngrams(pattern)  # Zerlegt das Muster in Phrasen (n-Gramme)
        all_phrases.extend(phrases)  # Fügt die Phrasen zur all_phrases-Liste hinzu
        xy.append((phrases, tag))  # Fügt das Phrase-Tag-Paar zur xy-Liste hinzu 

# Phrasen und Tags bereinigen---------------------------------------------------
ignore_phrases = ['?', '.', '!', ',']  # Liste der zu ignorierenden Phrasen (Satzzeichen)
all_phrases = [p for p in all_phrases if p not in ignore_phrases]  # Entfernt die zu ignorierenden Phrasen aus all_phrases
all_phrases = sorted(set(all_phrases))  # Sortiert und entfernt Duplikate in all_phrases
tags = sorted(set(tags))  # Sortiert und entfernt Duplikate in tags

# Trainingsdaten vorbereiten----------------------------------------------------
X_train = []  # Liste zur Speicherung der Bag-of-Phrases Repräsentationen der Eingabesätze
y_train = []  # Liste zur Speicherung der zugehörigen Tag-Labels
for (pattern_phrases, tag) in xy:  # Iteriert über jedes Phrase-Tag-Paar
    bag = bag_of_phrases(pattern_phrases, all_phrases)  # Wandelt den Eingabesatz in eine Bag-of-Phrases Repräsentation um.
    X_train.append(bag)  # Fügt die BoP zur X_train-Liste hinzu 
    label = tags.index(tag)  # Bestimmt den Index des aktuellen Tags in der Liste.
    y_train.append(label)  # Fügt den Index zur y_train-Liste hinzu

X_train = np.array(X_train)  # Wandelt X_train in ein numpy-Array um.
y_train = np.array(y_train)  # Wandelt y_train in ein numpy-Array um.

# Dataset-Klasse----------------------------------------------------------------
class ChatDataset(Dataset):  # Definiert eine benutzerdefinierte Dataset-Klasse
    def __init__(self, X_train, y_train):  # Initialisierungsmethode
        self.x_data = torch.tensor(X_train, dtype=torch.float32)  # Konvertiert X_train in einen Tensor
        self.y_data = torch.tensor(y_train, dtype=torch.long)  # Konvertiert y_train in einen Tensor
        self.n_samples = len(self.x_data)  # Speichert die Anzahl der Proben

    def __getitem__(self, index):  # Methode zum Abrufen einer einzelnen Probe
        return self.x_data[index], self.y_data[index]  # Gibt die Eingabedaten und das zugehörige Label zurück
    def __len__(self):  # Methode zur Bestimmung der Anzahl der Proben
        return self.n_samples  # Gibt die Anzahl der Proben zurück

# Dataset und DataLoader initialisieren  ---------------------------------------
dataset = ChatDataset(X_train, y_train)  # Erstellt ein Dataset-Objekt
train_loader = DataLoader(dataset, batch_size=8, shuffle=True, num_workers=0)  # Erstellt einen DataLoader für das Training
# Modell initialisieren---------------------------------------------------------
model = NeuralNet(len(X_train[0]), 8, len(tags)).to(device)  # Initialisiert das neuronale Netzwerk und verschiebt es auf das Gerät
criterion = nn.CrossEntropyLoss()  # Definiert die Verlustfunktion
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)  # Definiert den Optimierer

# Liste zur Speicherung des Verlusts pro Epoche
loss_values = []
# Trainingsschleife-------------------------------------------------------------
for epoch in range(1000):  # Iteriert über die Anzahl der Epochen  
    for words, labels in train_loader:  # Iteriert über die Batches im DataLoader
        words, labels = words.to(device), labels.to(device)  # Verschiebt die Eingabedaten und Labels auf das Gerät
        outputs = model(words)  # Führt eine Vorwärtsdurchlauf durch das Model aus 
        loss = criterion(outputs, labels)  # Berechnet den Verlust

        optimizer.zero_grad()  # Setzt die Gradienten auf null zurück
        loss.backward()  # Führt den Backpropagation-Schritt aus 
        optimizer.step()  # Aktualisiert die Modellparameter
        
    loss_values.append(loss.item())  # Speichere den Verlust pro Epoche

    if (epoch+1) % 100 == 0:  # Gibt den Verlust alle 100 Epochen aus
        print(f'Epoch [{epoch+1}/1000], Loss: {loss.item():.4f}')  # Druckt die aktuelle Epoche und den Verlust

# Modell und Metadaten speichern------------------------------------------------
model_info = {
    'model_state': model.state_dict(),  # Speichert den Zustand des Modells
    'input_size': len(X_train[0]),  # Speichert die Eingabegröße
    'hidden_size': 8,  # Größe des versteckten Layers
    'output_size': len(tags),  # Ausgabengröße
    'all_phrases': all_phrases,  # Alle Phrasen (n-Gramme)
    'tags': tags  # Alle Tags
}
torch.save(model_info, 'data.pth')  # Speichert das Model und die Metadaten in eine Datei 
print("Training complete. Model saved.")

# Verlustanalyse - Diagramm erstellen-------------------------------------------
plt.plot(range(1, 1001), loss_values, label='Loss')  # Erstellt eine Linie für den Verlustverlauf über die Epochen
plt.xlabel('Epochen')  # Beschriftung der x-Achse mit 'Epochen'
plt.ylabel('Verlust')  # Beschriftung der y-Achse mit 'Verlust'
plt.title('Verlust über die Epochen während des Trainings')  # Titel des Diagramms
plt.legend()  # Anzeige der Legende, um die Verlustkurve zu kennzeichnen
plt.grid(True)  # Aktiviert das Gitter für bessere Übersichtlichkeit des Diagramms
plt.show()  # Zeigt das Diagramm an

"""#  
Dieser Skript ist dafür entwickelt, ein neuronales Netzwerk für einen Chatbot zu trainieren.
Er beginnt damit, eine JSON-Datei zuladen, die verschiedenen Absichten (intents) enthält, wie z.B. Begrüßungen,
Fragen oder Anfragen, und die dazugehörigen möglichen Benutzeranfragen (patterns) und Antworten (responses).
Diese Muster werden dann in n-Gramme zerlegt und in eine Bag-of-Phrases-Repräsentation umgewandelt,
um die Eingabedaten für das Modell zu erstellen. Jede Absicht wird einem tag zugeordnet, das dem Modell als Ziel dient. 
Diese Daten werden in einem Dataset organisiert und mit Hilfe eines DataLoaders in Batches an das neuronale Netzwerk übergeben.
Das neuronale Netzwerk besteht aus einer Eingabeschicht, einer versteckten Schicht (mit 8 Neuronen) und einer Ausgabeschicht,
die die verschiedenen Tags vorhersagt. Mit einem Adam-Optimierer und einer Kreuzentropie-Verlustfunktion wird das Modell trainiert. 
Während des Trainings, das über 1000 Epochen läuft, wird der Verlust in jeder Epoche berechnet und gespeichert.
Nach dem Training wirs das Modell und die relevanten Metadaten gespeichert, damit es später für den Chatbot verwendet werden kann.  
Am Ende wird ein Diagramm erstellt, das den Verlustverlauf über die Epochen zeigt, um zu visualisieren,
wie gut das Modell gelernt hat, die Absichten korrekt zu klassifizieren."""

# Datenvorbereitung (Tokenisierung, Bag of Phrases): 30 Minuten
# Aufbau des neuronalen Netzwerks und dessen Initialisierung: 20 Minuten
# Einrichten des Datasets und DataLoader: 20 Minuten
# Implementierung der Trainingsloop (inklusive Verlustberechnung): 60 Minuten
# Speicherung des trainierten Modells und Metadaten: 15 Minuten
# Erstellung und Anzeige des Verlustdiagramms: 15 Minuten
# Gesamtdauer für train.py: Etwa 3.10 Stunden

# Chatbot-Entwicklung 8.45 Stunden


