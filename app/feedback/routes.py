# feedback/routes.py

from flask import Blueprint, request, jsonify, current_app
from .manager import FeedbackManager

feedback_bp = Blueprint('feedback', __name__)

@feedback_bp.route('/', methods=['POST'])  # Route relativ zum url_prefix '/feedback'
def handle_feedback():
    feedback_manager = FeedbackManager()
    data = request.get_json()

    if not data:
        current_app.logger.warning("Keine Daten bereitgestellt")
        return jsonify({'error': 'Keine Daten bereitgestellt'}), 400

    # Validierung der empfangenen Daten
    required_fields = ['rating', 'name', 'email', 'feedback']
    if not all(field in data for field in required_fields):
        current_app.logger.warning("Unvollständige Daten bereitgestellt")
        return jsonify({'error': 'Alle Felder müssen ausgefüllt sein'}), 400

    try:
        result = feedback_manager.save_feedback(data)
        current_app.logger.info(f"Feedback gespeichert: {result}")
        return jsonify(result), 200
    except Exception as e:
        current_app.logger.error(f"Fehler beim Speichern des Feedbacks: {e}")
        return jsonify({'error': 'Interner Serverfehler'}), 500


# setup_routes funktion:Richtet die Routen für das Blueprint ein.
# handle_feedback funktion: Handhabt POST-Anfragen für das Feedback.
# Initialisiert den Feedbackmanager.
# Gesamtdauer für die Bearbeitung: 25 Minuten

# Gesamtdauer der Bearbeitung Feedback: 1:30 Minuten



