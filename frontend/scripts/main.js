// Globale Variable für den Unterschriftsstatus
let hasSignature = false;

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
  document.getElementById('firstname').value = '';
  document.getElementById('lastname').value = '';
  if (document.getElementById('birthdate')) {
    document.getElementById('birthdate').value = '';
  }
  
  // Unterschrift zurücksetzen
  clearSignatureCanvas();
  
  // Unterschriftsstatus zurücksetzen
  hasSignature = false;
  
  // Lokalen Speicher leeren
  localStorage.removeItem('temp_user_data');
  
  // Validierungszustände zurücksetzen
  resetValidationStates();
  
  // Zur Startseite zurückkehren
  goToPage(1);
}

// Funktion für den "Zurück zum Start"-Button auf der letzten Seite
function resetAndGoToStart() {
  // Formularfelder zurücksetzen
  document.getElementById('firstname').value = '';
  document.getElementById('lastname').value = '';
  if (document.getElementById('birthdate')) {
    document.getElementById('birthdate').value = '';
  }
  
  // Unterschrift zurücksetzen
  clearSignatureCanvas();
  
  // Unterschriftsstatus zurücksetzen
  hasSignature = false;
  
  // Lokalen Speicher leeren
  localStorage.removeItem('temp_user_data');
  
  // Validierungszustände zurücksetzen
  resetValidationStates();
  
  // Zur Startseite zurückkehren
  goToPage(1);
}

// Funktion zum Zurücksetzen aller Validierungszustände
function resetValidationStates() {
  // Alle Next-Buttons auf den Eingabeseiten deaktivieren
  const inputPageButtons = document.querySelectorAll('#page2 .next-button, #page3 .next-button');
  inputPageButtons.forEach(button => {
    button.disabled = true;
  });
  
  // Submit-Button auf Seite 4 deaktivieren
  const submitButton = document.querySelector('#page4 .primary-button');
  if (submitButton) {
    submitButton.disabled = true;
  }
  
  // WEITER-Button auf Seite 6 aktivieren (dieser sollte immer klickbar sein)
  const page6Button = document.querySelector('#page6 .next-button');
  if (page6Button) {
    page6Button.disabled = false;
  }
  
  // Andere Buttons auf Informationsseiten aktivieren
  const infoPageButtons = document.querySelectorAll('#page1 .primary-button, #page8 .next-button, #page9 .primary-button');
  infoPageButtons.forEach(button => {
    button.disabled = false;
  });
}

// Canvas für Unterschrift löschen (per Button)
function clearSignatureCanvas() {
  const canvas = document.getElementById('signatureCanvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  
  // Unterschriftsstatus zurücksetzen
  hasSignature = false;
  
  // Submit-Button deaktivieren
  const submitButton = document.querySelector('#page4 .primary-button');
  if (submitButton) {
    submitButton.disabled = true;
  }
}

// Funktion zum Aktualisieren des Unterschrifts-Buttons
function updateSignatureButton() {
  const submitButton = document.querySelector('#page4 .primary-button');
  if (submitButton) {
    submitButton.disabled = !hasSignature;
  }
}

// Canvas für Unterschrift initialisieren
function initializeSignatureCanvas() {
  const canvas = document.getElementById('signatureCanvas');
  if (!canvas) return;
  
  // Unterschriftsstatus zurücksetzen
  hasSignature = false;
  
  // Submit-Button initial deaktivieren
  const submitButton = document.querySelector('#page4 .primary-button');
  if (submitButton) {
    submitButton.disabled = true;
  }
  
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

    // Unterschrift als vorhanden markieren
    hasSignature = true;
    
    // Submit-Button aktivieren
    const submitButton = document.querySelector('#page4 .primary-button');
    if (submitButton) {
      submitButton.disabled = false;
    }
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

// Funktion zum Absenden der Daten
function submitData() {
  // Daten sammeln
  const firstname = document.getElementById('firstname').value;
  const lastname = document.getElementById('lastname').value;
  const birthdate = document.getElementById('birthdate').value;
  
  // Signatur-Daten als blaue PNG
  const canvas = document.getElementById('signatureCanvas');
  
  // Spezielle Konvertierung für PNG mit blauer Signatur
  const signaturePng = canvas ? canvas.toDataURL('image/png') : null;
  
  // Daten-Objekt erstellen
  const userData = {
    firstname,
    lastname,
    birthdate,
    timestamp: new Date().toISOString()
  };
  
  // Daten als JSON und Signatur als Bild speichern
  saveUserData(userData, signaturePng);
  
  // Zur Ladeseite wechseln
  goToPage(5);
  
  // Simuliere Ladezeit (10 Sekunden) und gehe dann zur nächsten Seite
  setTimeout(() => {
    goToPage(6);
  }, 10000);
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

// Funktion zum Löschen der Benutzerdaten und Weiterleitung zur Danke-Seite
function deleteUserData() {
  try {
    // Formularfelder zurücksetzen
    document.getElementById('firstname').value = '';
    document.getElementById('lastname').value = '';
    if (document.getElementById('birthdate')) {
      document.getElementById('birthdate').value = '';
    }
    
    // Unterschrift zurücksetzen
    clearSignatureCanvas();
    
    // Unterschriftsstatus zurücksetzen
    hasSignature = false;
    
    // Lokale Daten löschen
    localStorage.removeItem('temp_user_data');
    
    // Validierungszustände zurücksetzen
    resetValidationStates();
    
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
        // Zur Danke-Seite weiterleiten
        goToPage(8);
      } else {
        throw new Error(data.message || 'Unbekannter Serverfehler');
      }
    })
    .catch(error => {
      console.error('Fehler beim Löschen der Daten vom Server:', error);
      alert('Die Daten konnten nicht gelöscht werden. Bitte versuchen Sie es später erneut.');
      // Trotz Fehler zur Danke-Seite weiterleiten
      goToPage(8);
    });
  } catch (error) {
    console.error('Fehler beim Löschen der Daten:', error);
    alert('Die Daten konnten nicht gelöscht werden. Bitte versuchen Sie es später erneut.');
    // Trotz Fehler zur Danke-Seite weiterleiten
    goToPage(8);
  }
}

// Funktion für X-Buttons: Löscht Daten und leitet zur Startseite weiter
function exitToHome() {
  try {
    // Formularfelder zurücksetzen
    document.getElementById('firstname').value = '';
    document.getElementById('lastname').value = '';
    if (document.getElementById('birthdate')) {
      document.getElementById('birthdate').value = '';
    }
    
    // Unterschrift zurücksetzen
    clearSignatureCanvas();
    
    // Unterschriftsstatus zurücksetzen
    hasSignature = false;
    
    // Lokale Daten löschen
    localStorage.removeItem('temp_user_data');
    
    // Validierungszustände zurücksetzen
    resetValidationStates();
    
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
        // Zur Startseite zurückkehren
        goToPage(1);
      } else {
        throw new Error(data.message || 'Unbekannter Serverfehler');
      }
    })
    .catch(error => {
      console.error('Fehler beim Löschen der Daten vom Server:', error);
      alert('Die Daten konnten nicht gelöscht werden. Bitte versuchen Sie es später erneut.');
      // Trotz Fehler zur Startseite zurückkehren
      goToPage(1);
    });
  } catch (error) {
    console.error('Fehler beim Löschen der Daten:', error);
    alert('Die Daten konnten nicht gelöscht werden. Bitte versuchen Sie es später erneut.');
    // Trotz Fehler zur Startseite zurückkehren
    goToPage(1);
  }
}

// Validierung für Pflichtfelder einrichten
function setupValidation() {
  // Validierung für Seite 2 (Name)
  const firstnameInput = document.getElementById('firstname');
  const lastnameInput = document.getElementById('lastname');
  if (firstnameInput && lastnameInput) {
    firstnameInput.addEventListener('input', () => validatePage(2));
    lastnameInput.addEventListener('input', () => validatePage(2));
    validatePage(2);
  }
  
  // Validierung für Seite 3 (Geburtsdatum)
  const birthdateInput = document.getElementById('birthdate');
  if (birthdateInput) {
    birthdateInput.addEventListener('input', () => validatePage(3));
    validatePage(3);
  }
  
  // Validierung für Seite 4 (Unterschrift)
  const canvas = document.getElementById('signatureCanvas');
  if (canvas) {
    // Validiere die Seite sofort, um den Button zu deaktivieren
    validatePage(4);
  }
}

// Validierung für eine bestimmte Seite durchführen
function validatePage(pageNumber) {
  let isValid = false;
  let nextButton;
  
  switch (pageNumber) {
    case 2: // Name-Seite
      const firstnameInput = document.getElementById('firstname');
      const lastnameInput = document.getElementById('lastname');
      isValid = firstnameInput && lastnameInput && firstnameInput.value.trim().length > 0 && lastnameInput.value.trim().length > 0;
      nextButton = document.querySelector('#page2 .next-button');
      break;
      
    case 3: // Geburtsdatum-Seite
      const birthdateInput = document.getElementById('birthdate');
      isValid = birthdateInput && birthdateInput.value.trim().length > 0;
      nextButton = document.querySelector('#page3 .next-button');
      break;
      
    case 4: // Unterschrift-Seite
      const canvas = document.getElementById('signatureCanvas');
      isValid = canvas && hasSignature;
      nextButton = document.querySelector('#page4 .primary-button'); // Korrekter Selektor für den Submit-Button
      break;
  }
  
  if (nextButton) {
    nextButton.disabled = !isValid;
  }
}