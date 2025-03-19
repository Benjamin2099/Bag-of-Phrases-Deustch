#app/chatbot/nltk_utils.py

import numpy as np 
import spacy

nlp = spacy.load('de_core_news_sm') # Lade das deutsche Sprachmodell von spaCy für NLP-Aufgaben.

def tokenize_to_ngrams(sentence, n=2):
    """ Tokenisiert den gegebenen Satz und erzeugt n-Gramme (Standard: bi-Gramme). """
    doc = nlp(sentence.lower())  # Tokenisiere und lemmatisiere den Satz
    tokens = [token.lemma_ for token in doc 
            if not token.is_punct and not token.is_space]  # Filtere Satzzeichen und Leerzeichen heraus 
    ngrams = [' '.join(tokens[i:i+n])     # Erzeuge n-Gramme (hier bi-Gramme, wenn n=2)
            for i in range(len(tokens)-n+1)] # Erzeugt n-Gramme (Gruppen von n aufeinanderfolgenden Wörtern), indem es n aufeinanderfolgende Token kombiniert.
    return ngrams

def bag_of_phrases(tokenized_sentence, phrases):
    """Erstellt einen Bag-of-Phrases Vektor für den tokenisierten Satz."""
    bag = np.zeros(len(phrases), dtype=np.float32) # Initialisiere einen Vektor (Bag-of-Phrases) mit Nullen, wobei die Länge dem der Phrasenliste entspricht.
    for idx, phrase in enumerate(phrases):  # Iteriert über alle Phrasen in der Liste `phrases`.
        if phrase in tokenized_sentence:  # Überprüft, ob die Phrase im tokenisierten Satz enthalten ist.
            bag[idx] = 1  # Setze den Wert an der entsprechenden Position im Vektor auf 1.
    return bag  # Gibt den BoP Vekto zurück.

"""
Lemmatisierung: Reduzierung eines Wortes auf seine Grundform.
Tokenisierung: Zerlegung eines Satzes in kleinere Bestandteile wie Wörter oder Zeichen.
"""
# Zeit für die Implementierung und Kommentierung: ca. 1.25 Minuten.

