import streamlit as st
from scoutAi import query_agent
import base64

# Konfiguration der Streamlit-Seite
st.set_page_config(
    page_title="ScoutingAI - Hochschule Aalen",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": """
            ## ScoutingAI - Hochschule Aalen
            Der KI-Assistent ScoutingAI wurde entwickelt, um bei der Talentsuche von Fußballspielern zu unterstützen.
        """
    }
)

# Initialisieren des Konversationskontexts, falls noch nicht vorhanden
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

# Sidebar
with st.sidebar:
    # Funktion zum Umwandeln eines Bildes in Base64
    def img_to_base64(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()

    # Laden und Anzeigen des Sidebar-Bildes mit Glüheffekt
    img_path = "imgs/sidebar_scouting_ai.png"
    img_base64 = img_to_base64(img_path)
    st.sidebar.markdown(
        f'<img src="data:image/png;base64,{img_base64}" alt="ScoutingAI Logo">',
        unsafe_allow_html=True,
    )
    st.sidebar.markdown("---")

    # Grundlegende Interaktionen in der Sidebar anzeigen
    st.sidebar.markdown("""
        ### Wissensstand
        Das Wissen des Tools umfasst die Bundesliga, 2. Bundesliga, 3. Bundesliga und die Saisons 2021-2024.

        ### Grundlegende Interaktionen

        Hier sind einige grundlegende Interaktionen, die du verwenden kannst:

        - **Abfrage einreichen:** Stelle eine Frage oder Anweisung, um eine Abfrage durchzuführen.
        - **Kein Chatbot:** Folgefragen werden nicht beantwortet.

        ### Beispiele für Abfragen:

        - *Wie viele Tore hat Harry Kane in der Saison 2023-2024 erzielt?*
        - *Welcher Spieler hat die meisten gelben Karten in der Saison 2023-2024?*
        - *Wie effizient ist Jamal Musiala beim Passen?*

        ### Schritte zur Verwendung:

        1. **Abfrage einreichen:** Gib deine Abfrage oder Anweisung in das Eingabefeld ein und drücke Enter.
        2. **Ergebnisse anzeigen:** Die Ergebnisse deiner Abfrage werden im Hauptbereich der Anwendung angezeigt.

        ### Hinweise:

        - Verwende präzise und klare Anweisungen für die Abfragen, um genaue Ergebnisse zu erhalten.
        - Je genauer die Frage, desto besser die Antwort.
        """)
    
    # Laden und Anzeigen des HS Aalen Logos
    hs_aalen_path = "imgs/hs-aalen.png"
    hs_aalen = img_to_base64(hs_aalen_path)
    st.sidebar.markdown(
        f'<img src="data:image/png;base64,{hs_aalen}" alt="Hochschule Aalen Logo">',
        unsafe_allow_html=True,
    )

# Überschrift der Hauptseite
st.header("GenAI für die Extraktion von Fußball-Daten")

# Benutzereingabe für den Chat
chat_input = st.chat_input("Frage mich etwas über Fußball:")
if chat_input:
    # Abfrage an den Agenten senden und Konversationshistorie aktualisieren
    result, st.session_state.conversation_history = query_agent(chat_input, st.session_state.conversation_history)

    # Letzten 20 Nachrichten in der Konversationshistorie anzeigen
    for message in st.session_state.conversation_history[-20:]:
        role = message["role"]
        
        # Nachricht im Chat-Format anzeigen
        with st.chat_message(role):
            st.write(message["content"])
