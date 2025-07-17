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
  
  // iOS-spezifische Anpassungen für Eingabefelder
  fixIOSInputs();
  
  // Idle-Modus initialisieren und sofort anzeigen (für Testing)
  initIdleMode(true);
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
  
  // Lokale Daten löschen
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
  ctx.lineWidth = 6; // Dickere Linie für bessere Sichtbarkeit
  ctx.lineCap = 'round';
  ctx.lineJoin = 'round';
  ctx.strokeStyle = '#000000'; // Schwarze Farbe für die Unterschrift
  
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
  
  // Starte die Abfrage des Druckstatus
  startPrintStatusPolling();
}

// Funktion zum Abfragen des Druckstatus
function startPrintStatusPolling() {
  console.log('Starte Abfrage des Druckstatus...');
  
  // Status-Polling-Intervall (alle 2 Sekunden)
  const statusInterval = setInterval(() => {
    console.log('Polling Druckstatus...');
    fetch('/print-status', {
      method: 'GET',
      headers: {
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache'
      }
    })
      .then(response => {
        if (!response.ok) {
          throw new Error('Netzwerkantwort war nicht ok');
        }
        return response.json();
      })
      .then(data => {
        console.log('Druckstatus erhalten:', data);
        
        // Status anzeigen
        const statusElement = document.getElementById('print-status-message');
        if (statusElement) {
          statusElement.textContent = data.message || 'Dokumente werden verarbeitet...';
        }
        
        // Bei "generating" Status anzeigen
        if (data.status === 'generating') {
          console.log('Druckvorgang läuft...');
          if (statusElement) {
            statusElement.textContent = 'Dokumente werden generiert und gedruckt...';
          }
        }
        
        // Bei "printing" Status anzeigen
        if (data.status === 'printing') {
          console.log('Dokumente werden gedruckt...');
          if (statusElement) {
            statusElement.textContent = 'Dokumente werden gedruckt...';
          }
        }
        
        // Bei Abschluss zur Erfolgsseite wechseln
        if (data.status === 'completed') {
          clearInterval(statusInterval);
          console.log('Druckvorgang abgeschlossen!');
          goToPage(6);
          showNotification('Druckvorgang abgeschlossen', 'Ihre Dokumente wurden erfolgreich gedruckt.');
        }
        
        // Bei Fehler auch zur Erfolgsseite wechseln, aber mit Fehlermeldung
        if (data.status === 'error') {
          clearInterval(statusInterval);
          console.error('Fehler beim Drucken:', data.message);
          goToPage(6);
          showNotification('Fehler beim Drucken', data.message || 'Es ist ein Fehler aufgetreten.');
          // Fehlermeldung anzeigen
          const errorElement = document.createElement('div');
          errorElement.className = 'error-message';
          errorElement.textContent = 'Es gab ein Problem beim Drucken. Bitte wenden Sie sich an einen Mitarbeiter.';
          document.getElementById('page6').appendChild(errorElement);
        }
      })
      .catch(error => {
        console.error('Fehler bei der Statusabfrage:', error);
      });
  }, 2000); // Alle 2 Sekunden abfragen
  
  // Sicherheitsmaßnahme: Nach 60 Sekunden automatisch zur Seite 6 wechseln, falls kein Status empfangen wurde
  setTimeout(() => {
    console.log('Timeout für Druckstatus-Polling erreicht');
    clearInterval(statusInterval);
    // Nur wechseln, wenn wir noch auf Seite 5 sind
    const currentPage = document.querySelector('.page.active');
    if (currentPage && currentPage.id === 'page5') {
      console.log('Wechsle automatisch zu Seite 6 nach Timeout');
      goToPage(6);
    }
  }, 60000);
}

// Funktion zum Anzeigen einer Desktop-Benachrichtigung
function showNotification(title, message) {
  // Prüfen, ob Browser-Benachrichtigungen unterstützt werden
  if ('Notification' in window) {
    // Berechtigung prüfen/anfordern
    if (Notification.permission === 'granted') {
      new Notification(title, { body: message });
    } else if (Notification.permission !== 'denied') {
      Notification.requestPermission().then(permission => {
        if (permission === 'granted') {
          new Notification(title, { body: message });
        }
      });
    }
  }
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
    });
    
    console.log('Daten erfolgreich im localStorage gespeichert und zum Server gesendet');
    
    // Ausgabe der Daten in der Konsole (zu Testzwecken)
    console.log('Gespeicherte Daten:', userData);
    
    // Erfolg melden
    return true;
  } catch (error) {
    console.error('Fehler beim Speichern der Daten:', error);
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
      // Trotz Fehler zur Danke-Seite weiterleiten
      goToPage(8);
    });
  } catch (error) {
    console.error('Fehler beim Löschen der Daten:', error);
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
      // Trotz Fehler zur Startseite zurückkehren
      goToPage(1);
    });
  } catch (error) {
    console.error('Fehler beim Löschen der Daten:', error);
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

// Funktion zur Behebung von iOS-Eingabeproblemen
function fixIOSInputs() {
  // Erkennen, ob es sich um ein iOS-Gerät handelt
  const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;
  
  if (isIOS) {
    console.log('iOS-Gerät erkannt, wende Eingabefeld-Fixes an');
    
    // Alle Textfelder und Datumsfelder auswählen
    const inputFields = document.querySelectorAll('input[type="text"], input[type="date"]');
    
    // Verhindere Scrollen auf der gesamten Seite
    document.addEventListener('touchmove', function(e) {
      e.preventDefault();
    }, { passive: false });
    
    // Spezielle Behandlung für Eingabefelder
    inputFields.forEach(input => {
      // Spezielle Behandlung für iOS-Eingabefelder
      input.setAttribute('autocomplete', 'off');
      input.setAttribute('autocorrect', 'off');
      input.setAttribute('autocapitalize', 'off');
      input.setAttribute('spellcheck', 'false');
      
      // Fokus explizit setzen beim Tippen
      input.addEventListener('touchend', function(e) {
        e.preventDefault();
        this.focus();
        this.click();
      });
      
      // Verhindern, dass der Fokus beim Scrollen verloren geht
      input.addEventListener('focus', function() {
        // Scrolle zu diesem Element (nur für dieses Element)
        const rect = this.getBoundingClientRect();
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        window.scrollTo({
          top: rect.top + scrollTop - 100,
          behavior: 'smooth'
        });
      });
    });
    
    // Spezielle Behandlung für das Datumsfeld
    const dateInput = document.getElementById('birthdate');
    if (dateInput) {
      dateInput.addEventListener('touchend', function(e) {
        e.preventDefault();
        // Verzögerung, um iOS Zeit zu geben
        setTimeout(() => {
          this.focus();
          this.click();
        }, 100);
      });
    }
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

/**
 * Idle Mode für die Kunst-KI Installation
 * Aktiviert einen Idle-Modus nach 15 Minuten Inaktivität
 * und kehrt mit einem Klick zum ersten Screen zurück
 */

// Konfiguration
const IDLE_TIMEOUT = 3 * 60 * 1000; // 3 Minuten in Millisekunden
let idleTimer = null;
let isIdle = false;

// DOM-Elemente
let idleScreen = null;

/**
 * Initialisierung des Idle-Modus
 * @param {boolean} showImmediately - Wenn true, wird der Idle-Modus sofort angezeigt
 */
function initIdleMode(showImmediately = true) {
  console.log('Initialisiere Idle-Modus...');
  
  // Idle-Screen erstellen
  createIdleScreen();
  
  // Event-Listener für Benutzeraktivität
  setupActivityListeners();
  
  // Timer starten
  resetIdleTimer();
  
  // Optional: Idle-Modus sofort anzeigen (für Testing)
  if (showImmediately) {
    console.log('Zeige Idle-Modus sofort an (Test-Modus)');
    setTimeout(enterIdleMode, 100); // Kurze Verzögerung, damit DOM vollständig geladen ist
  }
  
  console.log('Idle-Modus initialisiert. Timeout:', IDLE_TIMEOUT, 'ms');
}

/**
 * Erstellt den Idle-Screen als DOM-Element
 */
function createIdleScreen() {
  // Prüfen, ob der Idle-Screen bereits existiert
  if (document.getElementById('idle-screen')) {
    idleScreen = document.getElementById('idle-screen');
    return;
  }
  
  // Idle-Screen erstellen
  idleScreen = document.createElement('div');
  idleScreen.id = 'idle-screen';
  idleScreen.className = 'idle-screen';
  
  // Artifacts Wrapper erstellen (ähnlich wie buzz_wrapper)
  const artifactsWrapper = document.createElement('div');
  artifactsWrapper.className = 'artifacts_wrapper';
  
  // Text-Container erstellen
  const textDiv = document.createElement('div');
  textDiv.className = 'text';
  
  // Text "ARTIFACTS" hinzufügen
  const span = document.createElement('span');
  span.textContent = "ARTIFACTS";
  textDiv.appendChild(span);
  
  // Scanline hinzufügen
  const scanline = document.createElement('div');
  scanline.className = 'scanline';
  
  // Hinweistext hinzufügen - jetzt direkt im idle-screen, nicht im artifacts_wrapper
  const hintText = document.createElement('div');
  hintText.className = 'hint-text';
  hintText.textContent = "Bildschirm berühren um fortzufahren";
  
  // Elemente zusammenfügen
  artifactsWrapper.appendChild(textDiv);
  artifactsWrapper.appendChild(scanline);
  idleScreen.appendChild(artifactsWrapper);
  idleScreen.appendChild(hintText); // Hinweistext direkt zum idle-screen hinzufügen
  
  // Event-Listener zum Verlassen des Idle-Modus
  idleScreen.addEventListener('click', exitIdleMode);
  idleScreen.addEventListener('touchstart', exitIdleMode);
  
  // Zum Body hinzufügen
  document.body.appendChild(idleScreen);
  
  // Zusätzliche Spans für den Glitch-Effekt hinzufügen
  for (let i = 0; i < 4; i++) {
    const clonedSpan = span.cloneNode(true);
    textDiv.insertBefore(clonedSpan, textDiv.firstChild);
  }
  
  // Zusätzliche Scanlines hinzufügen
  for (let i = 0; i < 10; i++) {
    const clonedScanline = scanline.cloneNode(true);
    artifactsWrapper.appendChild(clonedScanline);
  }
}

/**
 * Setzt den Idle-Timer zurück
 */
function resetIdleTimer() {
  // Bestehenden Timer löschen
  if (idleTimer) {
    clearTimeout(idleTimer);
  }
  
  // Neuen Timer starten
  idleTimer = setTimeout(enterIdleMode, IDLE_TIMEOUT);
}

/**
 * Aktiviert den Idle-Modus
 */
function enterIdleMode() {
  if (isIdle) return; // Bereits im Idle-Modus
  
  console.log('Aktiviere Idle-Modus');
  isIdle = true;
  
  // Idle-Screen anzeigen
  idleScreen.style.display = 'flex';
  
  // Optional: Speichern des aktuellen Zustands
  saveCurrentState();
}

/**
 * Verlässt den Idle-Modus und kehrt zum ersten Screen zurück
 */
function exitIdleMode(event) {
  if (!isIdle) return; // Nicht im Idle-Modus
  
  console.log('Verlasse Idle-Modus');
  isIdle = false;
  
  // Idle-Screen ausblenden
  idleScreen.style.display = 'none';
  
  // Zum ersten Screen zurückkehren
  if (typeof resetAndGoToStart === 'function') {
    resetAndGoToStart();
  } else if (typeof resetAndGoHome === 'function') {
    resetAndGoHome();
  } else if (typeof goToPage === 'function') {
    goToPage(1);
  }
  
  // Timer zurücksetzen
  resetIdleTimer();
  
  // Verhindern, dass das Event weitergeleitet wird
  if (event) {
    event.preventDefault();
    event.stopPropagation();
  }
}

/**
 * Speichert den aktuellen Zustand der Anwendung
 * (optional, falls später benötigt)
 */
function saveCurrentState() {
  // Hier könnte der aktuelle Zustand gespeichert werden,
  // falls später eine Wiederherstellung gewünscht ist
}

/**
 * Richtet Event-Listener für Benutzeraktivität ein
 */
function setupActivityListeners() {
  // Liste der Events, die als Benutzeraktivität gelten
  const activityEvents = [
    'mousedown', 'mousemove', 'keydown',
    'touchstart', 'touchmove', 'touchend',
    'click', 'scroll', 'focus'
  ];
  
  // Event-Listener für jedes Event hinzufügen
  activityEvents.forEach(eventType => {
    document.addEventListener(eventType, handleUserActivity, { passive: true });
  });
}

/**
 * Behandelt Benutzeraktivität
 */
function handleUserActivity() {
  // Wenn im Idle-Modus, diesen verlassen
  if (isIdle) {
    exitIdleMode();
    return;
  }
  
  // Ansonsten nur den Timer zurücksetzen
  resetIdleTimer();
}