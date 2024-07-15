import streamlit as st
from scoutAi import query_agent
import base64

# Speicher für den Konversationskontext
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

# Streamlit Page Configuration
st.set_page_config(
    page_title="ScoutingAI - Hochschule Aalen",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": """
            ## ScoutingAI - Hochschule Aalen
            The AI Assistant, ScoutingAI, is designed to help in scouting football players.
        """
    }
)


# Sidebar
with st.sidebar:
    def img_to_base64(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()

    # Load and display sidebar image with glowing effect
    img_path = "imgs/sidebar_scouting_ai.png"
    img_base64 = img_to_base64(img_path)
    st.sidebar.markdown(
        f'<img src="data:image/png;base64,{img_base64}" >',
        unsafe_allow_html=True,
    )
    st.sidebar.markdown("---")

    st.sidebar.markdown("""
        ### Grundlegende Interaktionen

        Hier sind einige grundlegende Interaktionen, die du verwenden kannst:

        - **Abfrage einreichen:** Stelle eine Frage oder Anweisung, um eine Abfrage durchzuführen.
        - **Ergebnisse zusammenfassen:** Erstelle Zusammenfassungen oder Aggregationen der Daten.

        ### Beispiele für Abfragen:

        - *Wie viele Tore hat Harry Kane in der Saison 2023/2024 erzielt?*
        - *Berechne den Durchschnitt der Tore pro Spieler.*

        ### Schritte zur Verwendung:

        1. **Abfrage einreichen:** Gebe deine Abfrage oder Anweisung in das Eingabefeld ein und klicke auf "Abfrage einreichen".
        2. **Ergebnisse anzeigen:** Die Ergebnisse deiner Abfrage werden im Hauptbereich der Anwendung angezeigt.

        ### Hinweise:

        - Verwende präzise und klare Anweisungen für die Abfragen, um genaue Ergebnisse zu erhalten.
        - Nutze die Filter- und Sortierfunktionen, um spezifische Datenbereiche zu analysieren.

        Viel Spaß beim Erkunden deiner Daten!
        """)
    
    hs_aalen_path = "imgs/hs-aalen.png"
    hs_aalen = img_to_base64(hs_aalen_path)
    st.sidebar.markdown(
        f'<img src="data:image/png;base64,{hs_aalen}" >',
        unsafe_allow_html=True,
    )


        
st.header("GenAI für die Extraktion von Daten aus Fußball")

# User input for chat
chat_input = st.chat_input("Ask me about football:")
if chat_input:
    result, st.session_state.conversation_history = query_agent(chat_input, st.session_state.conversation_history)

    for message in st.session_state.conversation_history[-20:]:
        role = message["role"]
        
        with st.chat_message(role):
            st.write(message["content"])