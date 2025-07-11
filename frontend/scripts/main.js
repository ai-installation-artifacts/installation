// Beim Laden der Seite die erste Seite anzeigen
document.addEventListener('DOMContentLoaded', function() {
  console.log('DOM vollständig geladen');
  // Standardmäßig Seite 1 anzeigen
  goToPage(1);
  
  // Canvas für Unterschrift initialisieren
  initializeSignatureCanvas();
  
  // Validierung für Pflichtfelder einrichten
  setupValidation();
});

// Funktion zum Wechseln zwischen Seiten
function goToPage(pageNumber) {
  console.log('Navigiere zu Seite:', pageNumber);
  
  // Alle Seiten ausblenden und active-Klasse entfernen
  const pages = document.querySelectorAll('.page');
  pages.forEach(page => {
    page.style.display = 'none';
    page.classList.remove('active');
  });
  
  // Die ausgewählte Seite anzeigen und active-Klasse hinzufügen
  const selectedPage = document.getElementById('page' + pageNumber);
  if (selectedPage) {
    selectedPage.style.display = 'flex';
    selectedPage.classList.add('active');
    console.log('Seite gefunden und angezeigt:', pageNumber);
  } else {
    console.error('Seite nicht gefunden:', pageNumber);
  }
}

// Funktion zum Zurücksetzen und zur Startseite gehen
function resetAndGoHome() {
  // Formularfelder zurücksetzen
  document.getElementById('name').value = '';
  if (document.getElementById('birthdate')) {
    document.getElementById('birthdate').value = '';
  }
  
  // Zur Startseite zurückkehren
  goToPage(1);
}

// Funktion zum Absenden der Daten
function submitData() {
  // Daten sammeln
  const name = document.getElementById('name').value;
  const birthdate = document.getElementById('birthdate').value;
  
  // Signatur-Daten als blaue PNG
  const canvas = document.getElementById('signatureCanvas');
  
  // Spezielle Konvertierung für PNG mit blauer Signatur
  const signaturePng = canvas ? canvas.toDataURL('image/png') : null;
  
  // Daten-Objekt erstellen
  const userData = {
    name,
    birthdate,
    timestamp: new Date().toISOString()
  };
  
  // Daten als JSON und Signatur als Bild speichern
  saveUserData(userData, signaturePng);
  
  // Zur Ladeseite wechseln
  goToPage(5);
  
  // Simuliere Ladezeit (3 Sekunden) und gehe dann zur nächsten Seite
  setTimeout(() => {
    goToPage(6);
  }, 3000);
}

// Funktion zum Speichern der Benutzerdaten als JSON
function saveUserData(userData, signaturePng) {
  try {
    // JSON-String erstellen
    const jsonData = JSON.stringify(userData, null, 2);
    
    // Daten im localStorage speichern (für lokale Referenz)
    localStorage.setItem('temp_user_data', jsonData);
    
    // Signatur als Base64 ohne Header vorbereiten
    let base64Signature = null;
    if (signaturePng) {
      base64Signature = signaturePng.split(',')[1]; // Entferne den MIME-Header
    }
    
    // Daten an den Server senden
    fetch('/save-user-data', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        userData: userData,
        signature: base64Signature
      })
    })
    .then(response => response.json())
    .then(data => {
      console.log('Server-Antwort:', data);
    })
    .catch(error => {
      console.error('Fehler bei der Serveranfrage:', error);
      alert('Die Daten konnten nicht zum Server gesendet werden.');
    });
    
    console.log('Daten erfolgreich im localStorage gespeichert und zum Server gesendet');
    
    // Ausgabe der Daten in der Konsole (zu Testzwecken)
    console.log('Gespeicherte Daten:', userData);
    
    // Erfolg melden
    return true;
  } catch (error) {
    console.error('Fehler beim Speichern der Daten:', error);
    alert('Die Daten konnten nicht gespeichert werden. Bitte versuchen Sie es später erneut.');
    return false;
  }
}

// Funktion zum Löschen der Benutzerdaten
function deleteUserData() {
  try {
    // Lokale Daten löschen
    localStorage.removeItem('temp_user_data');
    
    // Server-Anfrage zum Löschen aller Daten im data-Ordner
    fetch('/delete-user-data', {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(response => response.json())
    .then(data => {
      console.log('Server-Antwort:', data);
      if (data.status === 'success') {
        console.log('Alle Daten wurden erfolgreich vom Server gelöscht');
        // Zur Bestätigungsseite wechseln
        goToPage(8);
      } else {
        throw new Error(data.message || 'Unbekannter Serverfehler');
      }
    })
    .catch(error => {
      console.error('Fehler beim Löschen der Daten vom Server:', error);
      alert('Die Daten konnten nicht gelöscht werden. Bitte versuchen Sie es später erneut.');
    });
  } catch (error) {
    console.error('Fehler beim Löschen der Daten:', error);
    alert('Die Daten konnten nicht gelöscht werden. Bitte versuchen Sie es später erneut.');
  }
}

// Canvas für Unterschrift löschen (per Button)
function clearSignatureCanvas() {
  const canvas = document.getElementById('signatureCanvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  canvas.dataset.signed = 'false';
}

// Canvas für Unterschrift initialisieren
function initializeSignatureCanvas() {
  const canvas = document.getElementById('signatureCanvas');
  if (!canvas) return;
  
  const ctx = canvas.getContext('2d');
  let isDrawing = false;
  let lastX = 0;
  let lastY = 0;
  
  // Stift-Einstellungen
  ctx.lineWidth = 2;
  ctx.lineCap = 'round';
  ctx.lineJoin = 'round';
  ctx.strokeStyle = '#0000FF'; // Blaue Farbe für die Unterschrift
  
  // Event-Listener für Maus
  canvas.addEventListener('mousedown', (e) => {
    const { x, y } = getCanvasCoords(e, canvas);
    startDrawing(x, y);
  });
  canvas.addEventListener('mousemove', (e) => {
    if (!isDrawing) return;
    const { x, y } = getCanvasCoords(e, canvas);
    draw(x, y);
  });
  canvas.addEventListener('mouseup', stopDrawing);
  canvas.addEventListener('mouseout', stopDrawing);

  // Touch-Events
  canvas.addEventListener('touchstart', (e) => {
    e.preventDefault();
    const touch = e.touches[0];
    const { x, y } = getCanvasCoords(touch, canvas);
    startDrawing(x, y);
  });
  canvas.addEventListener('touchmove', (e) => {
    e.preventDefault();
    if (!isDrawing) return;
    const touch = e.touches[0];
    const { x, y } = getCanvasCoords(touch, canvas);
    draw(x, y);
  });
  canvas.addEventListener('touchend', stopDrawing);
  
  function startDrawing(x, y) {
    isDrawing = true;
    lastX = x;
    lastY = y;
  }

  function draw(x, y) {
    if (!isDrawing) return;

    ctx.beginPath();
    ctx.moveTo(lastX, lastY);
    ctx.lineTo(x, y);
    ctx.stroke();

    lastX = x;
    lastY = y;

    // Unterschrift als vorhanden markieren für Validierung
    canvas.dataset.signed = 'true';
    validatePage(4);
  }
  
  function stopDrawing() {
    isDrawing = false;
  }
  
  // Hilfsfunktion: Berechnet die Canvas-Koordinaten aus Maus- oder Touch-Event
  function getCanvasCoords(e, canvas) {
    const rect = canvas.getBoundingClientRect();
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;
    let x, y;
    if ('clientX' in e && 'clientY' in e) {
      x = (e.clientX - rect.left) * scaleX;
      y = (e.clientY - rect.top) * scaleY;
    } else {
      x = 0;
      y = 0;
    }
    return { x, y };
  }
}

// Validierung für Pflichtfelder einrichten
function setupValidation() {
  // Validierung für Seite 2 (Name)
  const nameInput = document.getElementById('name');
  if (nameInput) {
    nameInput.addEventListener('input', () => validatePage(2));
    validatePage(2);
  }
  
  // Validierung für Seite 3 (Geburtsdatum)
  const birthdateInput = document.getElementById('birthdate');
  if (birthdateInput) {
    birthdateInput.addEventListener('input', () => validatePage(3));
    validatePage(3);
  }
}

// Validierung für eine bestimmte Seite durchführen
function validatePage(pageNumber) {
  let isValid = false;
  let nextButton;
  
  switch (pageNumber) {
    case 2: // Name-Seite
      const nameInput = document.getElementById('name');
      isValid = nameInput && nameInput.value.trim().length > 0;
      nextButton = document.querySelector('#page2 .next-button');
      break;
      
    case 3: // Geburtsdatum-Seite
      const birthdateInput = document.getElementById('birthdate');
      isValid = birthdateInput && birthdateInput.value.trim().length > 0;
      nextButton = document.querySelector('#page3 .next-button');
      break;
      
    case 4: // Unterschrift-Seite
      const canvas = document.getElementById('signatureCanvas');
      isValid = canvas && canvas.dataset.signed === 'true';
      nextButton = document.querySelector('#page4 .next-button');
      break;
  }
  
  if (nextButton) {
    nextButton.disabled = !isValid;
  }
}