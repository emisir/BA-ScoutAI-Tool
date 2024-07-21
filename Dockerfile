# Verwenden Sie ein Python-Basis-Image
FROM python:3.9

# Installieren Sie Google Chrome
RUN apt-get update && apt-get install -y wget gnupg \
    && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Setzen Sie Umgebungsvariablen für Chrome
ENV CHROME_BIN=/usr/bin/google-chrome

# Setzen Sie das Arbeitsverzeichnis
WORKDIR /app

# Kopieren Sie die requirements.txt und installieren Sie die Abhängigkeiten
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopieren Sie den restlichen Code
COPY . .

# Starten Sie das Skript
CMD sh -c 'streamlit run app.py'
