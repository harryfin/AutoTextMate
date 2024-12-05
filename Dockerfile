FROM python:3

# Arbeitsverzeichnis im Container
WORKDIR /app

# Kopiere die Abhängigkeitsdatei in den Container
COPY requirements.txt requirements.txt

# Kopiere die notes
COPY notes notes

# Installiere die Abhängigkeiten
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere das Python-Skript in den Container
COPY auto_text_mate.py auto_text_mate.py

# Standardbefehl
CMD ["python", "auto_text_mate.py"]
