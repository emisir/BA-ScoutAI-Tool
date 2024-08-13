# GenAI Tool für Bachelorarbeit

Dieses Repository enthält das GenAI Tool, das im Rahmen meiner Bachelorarbeit entwickelt wurde.

## Inhalt

- [Überblick](#überblick)
- [Installation](#installation)
- [Verwendung](#verwendung)

## Überblick

Das GenAI Tool wurde entwickelt, um den Einsatz von generativer künstlicher Intelligenz im Fußball zu demonstrieren.

## Installation

Um das GenAI Tool lokal auf Ihrem Rechner zu installieren, folgen Sie bitte diesen Schritten:

1. Klonen Sie das Repository:

    ```bash
    git clone https://github.com/emisir/BA-GenAI-Tool.git
    ```

2. Navigieren Sie in das Projektverzeichnis:

    ```bash
    cd BA-GenAI-Tool
    ```

4. Erstellen und aktivieren Sie eine virtuelle Umgebung:

    ```bash
    python3 -m venv env
    source env/bin/activate  # Für Windows: env\Scripts\activate
    ```
   
5. Installieren Sie die erforderlichen Abhängigkeiten:

   ```bash
   pip install -r requirements.txt
   ```
   
## Verwendung

Nach der Installation können Sie das GenAI Tool über Streamlit starten:

   ```bash
   streamlit run app.py
   ```

Dieser Befehl startet das Tool und öffnet die Anwendung in Ihrem Standard-Webbrowser.
