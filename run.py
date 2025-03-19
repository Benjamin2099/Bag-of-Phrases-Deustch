# run.py
#chatbot_env\Scripts\activate
#source chatbot_env/bin/activate
#deactivate
import os
from app import create_app  # Import von create_app aus dem app-Paket

# Erstelle die Flask-App-Instanz
app = create_app()

if __name__ == '__main__':
    # Debug-Modus ist aktiviert, wenn die Umgebungsvariable `FLASK_DEBUG` auf 'true' gesetzt ist
    debug_mode = os.environ.get('FLASK_DEBUG', 'True').lower() in ['true', '1']
    
    # Host und Port aus Umgebungsvariablen abrufen oder Standardwerte verwenden
    host = os.environ.get('FLASK_HOST', '127.0.0.1')
    port = int(os.environ.get('FLASK_PORT', '5000'))
    
    # Aufruf von app.run() mit Parametern für Debugging, Host und Port
    app.run(debug=debug_mode, host=host, port=port)





