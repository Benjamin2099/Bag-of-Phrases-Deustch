
# tests/chatbot/test_nlp_utils.py
#https://stackoverflow.com/questions/67870861/problems-to-use-python-unittest-mock-properly
#https://stackoverflow.com/questions/71348957/python-unittest-mocking-problems-global-variable
import unittest
from app.chatbot.nltk import tokenize_to_ngrams, bag_of_phrases  # Importiere die Funktionen, die getestet werden sollen

class TestNLPUtils(unittest.TestCase):
    """
    Testklasse für die NLP-Hilfsfunktionen, um sicherzustellen, dass 
    die Tokenisierungs- und Bag-of-Phrases-Funktionen korrekt arbeiten.
    """
    def test_tokenize_to_bigrams(self):
        """
        Überprüft, ob die Funktion aus einem Beispieltext die erwarteten bi-Gramme erstellt.
        """
        text = "Hallo, wie geht es Ihnen heute?"
        erwartet = ['hallo wie', 'wie gehen', 'gehen es', 'es ihnen', 'ihnen heute']
        # Aufruf der Funktion zur Erstellung von bi-Grammen
        result = tokenize_to_ngrams(text, n=2)
        # Überprüft, ob das Ergebnis den Erwartungen entspricht
        self.assertEqual(result, erwartet, f"Erwartet: {erwartet}, aber erhalten: {result}")

    def test_bag_of_phrases_vector(self):
        """
        Überprüft, ob der Vektor korrekt angibt, welche Phrasen im Satz vorhanden sind.
        """
        bekannte_phrasen = ['hallo wie', 'geht es', 'ihnen heute']
        tokenisierter_satz = ['hallo wie', 'geht es']
        erwartet = [1, 1, 0]
        # Aufruf der Funktion zur Erstellung des Bag-of-Phrases Vektors
        result = bag_of_phrases(tokenisierter_satz, bekannte_phrasen)
        # Überprüft, ob das Ergebnis mit dem erwarteten Vektor übereinstimmt
        self.assertTrue((result == erwartet).all(), f"Erwarteter Vektor: {erwartet}, aber erhalten: {result.tolist()}")

    def test_tokenize_to_ngrams_with_empty_input(self):
        """
        Testet `tokenize_to_ngrams` mit einem leeren Satz und prüft, ob eine leere Liste zurückgegeben wird.
        """
        text = ""
        erwartet = []
        # Überprüft, ob die Funktion eine leere Liste zurückgibt
        result = tokenize_to_ngrams(text, n=2)
        self.assertEqual(result, erwartet, "Ein leerer Text sollte eine leere Liste zurückgeben.")

    def test_bag_of_phrases_with_empty_tokenized_sentence(self):
        """
        Testet `bag_of_phrases` mit einer leeren tokenisierten Liste und erwartet einen Vektor mit Nullen.
        """
        bekannte_phrasen = ['hallo wie', 'geht es', 'ihnen heute']
        tokenisierter_satz = []
        erwartet = [0, 0, 0]
        # Überprüft, ob der Bag-of-Phrases Vektor nur Nullen enthält
        result = bag_of_phrases(tokenisierter_satz, bekannte_phrasen)
        self.assertTrue((result == erwartet).all(), "Bei leerem tokenisiertem Satz sollte der Vektor nur Nullen enthalten.")

if __name__ == '__main__':
    unittest.main()

"""
Leere Eingaben sind Sonderfälle, die in der Praxis häufig vorkommen können, z. B. durch Benutzerfehler oder unerwartete Eingabedaten. 
Durch das Testen solcher Fälle wird sichergestellt, 
dass die Funktionen stabil und robust sind und dass sie bei solchen Eingaben vorhersehbare und kontrollierte Ergebnisse liefern.
"""
# Zeit für die Tests: ca. 1,24 Stunde