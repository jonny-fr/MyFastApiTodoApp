# Dockerfile

# 1. Basis-Image auswählen
# Wir starten mit einem offiziellen Python-Image (Version 3.9 in diesem Fall)
# Die "slim"-Variante ist kleiner als die Standardvariante.
FROM python:3.9-slim

# 2. Arbeitsverzeichnis im Container setzen
# Alle folgenden Befehle werden relativ zu diesem Verzeichnis ausgeführt.
WORKDIR /app

# 3. Abhängigkeiten kopieren und installieren
# Kopiere zuerst nur die requirements.txt, um Docker"s Layer Caching zu nutzen.
# Wenn sich requirements.txt nicht ändert, muss pip install nicht erneut ausgeführt werden.
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 4. Anwendungs-Code in den Container kopieren
# Kopiere den gesamten Inhalt des aktuellen Verzeichnisses (wo das Dockerfile liegt)
# in das Arbeitsverzeichnis /app im Container.
COPY . .

# 5. Port freigeben (nur zur Information)
# Teile Docker mit, dass der Container auf Port 80 lauschen wird.
# Dies öffnet den Port nicht tatsächlich nach außen, das passiert beim `docker run`.
EXPOSE 80

# 6. Startbefehl definieren
# Der Befehl, der ausgeführt wird, wenn ein Container aus diesem Image gestartet wird.
# Wir starten Uvicorn, binden es an 0.0.0.0 (wichtig!), um von außen erreichbar zu sein,
# auf Port 80 und geben die FastAPI-App-Instanz an (main:app).
# Die Anzahl der Worker kann angepasst werden (hier 4).
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--workers", "4"]


#build:
# docker build -t fastapi_image .

#run:
# docker run -d -p 80:80 --name fastapi_app fastapi_image