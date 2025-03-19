
/* JavaScript-Code für die Interaktionen innerhalb der Webanwendung.

   - Initialisierung und Setup der Event Listener: 40 minute
   - Implementierung der Chat-Funktionalität: 42 Minute
   - Integration mit dem Backend und Fehlerbehandlung: 45 Minute
   - Tests und Debugging: 1 Stunde
   - Gesamtschätzung: 3:07 Stunden
*/
// Warten auf das vollständige Laden des DOMs bevor JavaScript ausgeführt wird
document.addEventListener('DOMContentLoaded', function () {
    // Selektiert die Chatbox für weitere Manipulationen
    const chatbox = document.querySelector('.chatbox');
    const chatboxButton = document.querySelector('.chatbox__button button');
    const chatboxSupport = document.querySelector('.chatbox__support');
    const sendButton = document.querySelector('.send__button');
    const chatInput = document.querySelector('.chatbox__footer input');
    const chatMessages = document.querySelector('.chatbox__messages');

    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Einfacheres Ein-/Ausblenden der Chatbox ohne jQuery
    window.addEventListener('scroll', function() {
        const scroll = window.scrollY;
        chatbox.style.display = (scroll >= 100) ? 'block' : 'none';
    });

    chatboxButton.addEventListener('click', function () {
        chatboxSupport.classList.toggle('chatbox--active');
        scrollToBottom();
    });

    sendButton.addEventListener('click', function () {
        const messageText = chatInput.value.trim();
        if (!messageText) return;

        const messageItem = document.createElement('div');
        messageItem.classList.add('messages__item', 'messages__item--visitor');
        messageItem.textContent = messageText;
        chatMessages.appendChild(messageItem);
        chatInput.value = '';
        scrollToBottom();
         
        fetch('/chatbot/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ message: messageText })
        })
        .then(response => response.json())// Verarbeitet die Antwort des Servers
        .then(data => {
            const responseItem = document.createElement('div');// Erstellt ein Div für die Antwort
            responseItem.classList.add('messages__item', 'messages__item--operator');
            responseItem.textContent = data.response;// Setzt den Antworttext
            chatMessages.appendChild(responseItem);// Fügt die Antwort dem Nachrichtenbereich hinzu
            scrollToBottom();// Scrollt nach unten, um die Antwort anzuzeigen
        })
        .catch(error => {
            console.error('Error:', error);// Fängt Fehler bei der Anfrage ab
            alert('Es gab ein Problem mit dem Senden Ihrer Nachricht.');
        });
    });
// Event-Listener für den Feedback-Button zum Ein-/Ausblenden des Feedback-Formulars
        document.getElementById('feedbackButton').addEventListener('click', function() {
            const form = document.getElementById('feedbackForm');
            form.classList.toggle('feedback--active');
        });

// Event-Listener für Emoji-Auswahl im Feedback-Formular
    document.querySelectorAll('.emoji').forEach(emoji => {
        emoji.addEventListener('click', function() {
            document.getElementById('feedbackRating').value = this.getAttribute('data-value');
            // Setzt visuelles Feedback für das ausgewählte Emoji
            document.querySelectorAll('.emoji').forEach(e => e.style.opacity = '0.5');
            this.style.opacity = '1.0';
        });
    });
});
// Funktion zum Senden des Feedbacks
function sendFeedback() {
    const rating = document.getElementById('feedbackRating').value;
    const name = document.getElementById('feedbackName').value;
    const email = document.getElementById('feedbackEmail').value;
    const text = document.getElementById('feedbackText').value;
// Überprüft, ob alle Felder ausgefüllt sind
    if (!rating || !name || !email || !text) {
        alert('Bitte füllen Sie alle Felder aus und wählen Sie eine Bewertung.');
        return;
    }
// Sendet das Feedback an den Server
    fetch('http://127.0.0.1:5000/feedback/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ rating, name, email, feedback: text })
    })
    .then(response => response.json())// Verarbeitet die Antwort
    .then(data => {
        alert('Feedback gesendet: ' + data.message);// Zeigt eine Bestätigungsnachricht
        document.getElementById('feedbackForm').style.display = 'none';// Blendet das Formular aus
    })
.catch(error => {
    console.error('Error:', error);
    alert(`Es gab ein Problem mit dem Senden Ihres Feedbacks: ${error.message}`);
});
}
