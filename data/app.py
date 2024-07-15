import streamlit as st
import base64
from main import query_agent  # Importiere die Funktion zum Abfragen des Agenten
# from chat import football_agent

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

# CSS für das Glow-Effekt
st.markdown(
    """
    <style>
    .cover-glow {
        width: 100%;
        height: auto;
        padding: 3px;
        box-shadow: 
            0 0 5px #003366,
            0 0 10px #0066CC,
            0 0 15px #0099FF,
            0 0 20px #33CCFF,
            0 0 25px #66FFFF,
            0 0 30px #99FFFF,
            0 0 35px #CCFFFF;
        position: relative;
        z-index: -1;
        border-radius: 30px;
    }
    </style>
    """,
    unsafe_allow_html=True,
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
        f'<img src="data:image/png;base64,{img_base64}" class="cover-glow">',
        unsafe_allow_html=True,
    )
    st.sidebar.markdown("---")

    show_basic_info = st.sidebar.checkbox("Show Basic Interactions", value=True)

    # Display basic interactions info if toggled
    if show_basic_info:
        st.sidebar.markdown("""
        ### Basic Interactions
        - **Ask About ScoutingAI**: Type your questions about ScoutingAI's functionalities, player data, or general scouting tips.
        - **Search for Players**: Use keywords like 'player stats', 'top players', or 'scouting reports' to get relevant information.
        - **Navigate Updates**: Switch to 'Updates' mode to browse the latest features and improvements in ScoutingAI.
        """)

    show_advanced_info = st.sidebar.checkbox("Show Advanced Interactions", value=False)

    if show_advanced_info:
        st.sidebar.markdown("""
        ### Advanced Interactions
        - **Generate a Scouting Report**: Use keywords like **generate report**, **create scouting report** to get a detailed scouting report on a player.
        - **Player Analysis**: Ask for **player analysis**, **performance review** to understand the strengths and weaknesses of a player.
        - **Team Analysis**: Use **analyze team**, **team performance** to get insights and recommendations on team performance.
        - **Scouting Tips**: Use **scouting tips**, **recruitment strategies** to get help with effective scouting and recruitment strategies.
        """)

st.header("GenAI für die Extraktion von Daten aus Fußball")

# Benutzereingabe
user_input = st.chat_input("Ask me something about Football:")

if user_input:
    result, st.session_state.conversation_history = query_agent(user_input, st.session_state.conversation_history)
        
    for msg in st.session_state.conversation_history:
        if msg['role'] == "user":
            st.markdown(f"<div style='text-align: right;'><b>Du:</b> {msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='text-align: left;'><b>ScoutingAI:</b> {msg['content']}</div>", unsafe_allow_html=True)
