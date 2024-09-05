# Verwende ein offizielles Python-Image als Basis
FROM python:3.9-slim

# Installiere notwendige Systempakete
RUN apt-get update && apt-get install -y \
    x11-apps \
    xclip \
    && rm -rf /var/lib/apt/lists/*

# Setze das Arbeitsverzeichnis auf /usr/src/app
WORKDIR /usr/src/app

# Kopiere die requirements.txt in das Image
COPY requirements.txt .

# Installiere die Python-Abhängigkeiten aus der requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere das Python-Skript in das Arbeitsverzeichnis
COPY paste_script.py .

# Setze den Befehl, der beim Start des Containers ausgeführt wird
CMD ["python", "paste_script.py"]
