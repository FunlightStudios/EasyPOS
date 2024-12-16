# Modern POS System

# ⚠️ Work in Progress
This project is under active development and not production-ready yet.

Ein modernes Point of Sale System entwickelt mit Python und PySide6.

## Features

- 🛍️ Intuitive Verkaufsoberfläche
- 💰 Mehrere Zahlungsmethoden (Bar, Karte, TWINT)
- 📦 Lagerverwaltung mit Mindestbestandswarnung
- 📊 Detaillierte Berichte und Analysen
- 🎨 Modernes Dark Theme
- 🔒 Sicheres Benutzermanagement
- 🖨️ Rechnungs- und Belegdruck
- 💱 Flexible Währungseinstellungen
- 🔄 Automatische Datensicherung

## Installation

1. Python 3.11+ installieren
2. Repository klonen
3. Virtuelle Umgebung erstellen:
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

4. Abhängigkeiten installieren:
```bash
pip install -r requirements.txt
```

5. Umgebungsvariablen konfigurieren:
```bash
cp .env.example .env
# .env Datei nach Bedarf anpassen
```

6. Datenbank initialisieren:
```bash
python create_admin.py  # Erstellt Admin-Benutzer
```

7. Anwendung starten:
```bash
python main.py
```

## Entwicklung

- Python 3.11+
- PySide6 für die GUI
- SQLAlchemy für Datenbankoperationen
- Alembic für Datenbankmigrationen
- ReportLab für PDF-Generierung

## Lizenz

Copyright 2023 Codeium
