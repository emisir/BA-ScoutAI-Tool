from llama_index.core.query_pipeline import (
    QueryPipeline as QP,
    Link,
    InputComponent as InputComponent,
)
from llama_index.experimental.query_engine.pandas import PandasInstructionParser as PandasInstructionParser
from llama_index.llms.openai import OpenAI
from llama_index.core.prompts import PromptTemplate as PromptTemplate
import pandas as pd
import os
import streamlit as st

api_key = st.secrets["api_key"]["OPENAI_API_KEY"]

# Verzeichnis, in dem sich die CSV-Dateien befinden
data_dir = "csv"

# Liste zum Speichern der einzelnen DataFrames
dataframes_list = []

# Durchlaufen aller Dateien im Verzeichnis "data_dir"
for filename in os.listdir(data_dir):
    # Überprüfen, ob die Datei eine CSV-Datei ist
    if filename.endswith(".csv"):
        file_path = os.path.join(data_dir, filename)
        print(f"Loading CSV file: {file_path}")
        
        # Extrahieren von Liga und Saison aus dem Dateinamen
        parts = filename.replace(".csv", "").split("_")
        league = parts[0]
        season = parts[-1]
        
        # Laden der CSV-Datei in einen DataFrame
        single_df = pd.read_csv(file_path)
        # Hinzufügen der Saison- und Liga-Informationen als neue Spalten
        single_df['Season'] = season
        single_df['League'] = league
        # Hinzufügen des DataFrames zur Liste
        dataframes_list.append(single_df)

# Zusammenführen aller DataFrames in einen großen DataFrame
df = pd.concat(dataframes_list, ignore_index=True)
print(df.head())  

# Auf Deutsch übersetzt
# Anweisungen zur Umwandlung der Anfrage in ausführbaren Pandas-Code
instruction_str = (
    "1. Konvertiere die Anfrage in ausführbaren Python-Code unter Verwendung von Pandas.\n"
    "2. Die letzte Codezeile sollte ein Python-Ausdruck sein, der mit der eval() Funktion aufgerufen werden kann.\n"
    "3. Der Code sollte eine Lösung für die Anfrage darstellen.\n"
    "4. DRUCKE NUR DEN AUSDRUCK\n"
    "5. Zitiere den Ausdruck nicht.\n"
)

# Vorlage für den Pandas-Prompt
pandas_prompt_str = (
    "Sie arbeiten mit einem Pandas DataFrame in Python.\n"
    "Der Name des DataFrames ist df.\n"
    "Dies ist das Ergebnis von print(df.head()):\n"
    "{df_str}\n\n"
    "Befolgen Sie diese Anweisungen:\n"
    "{instruction_str}\n"
    "Anfrage: {query_str}\n\n"
    "Ausdruck:"
)

# Vorlage für die Synthese der Antwort
response_synthesis_prompt_str = (
    "Geben Sie basierend auf einer Eingabefrage eine Antwort aus den Abfrageergebnissen.\n"
    "Anfrage: {query_str}\n\n"
    "Pandas-Anweisungen (optional):\n{pandas_instructions}\n\n"
    "Pandas-Ausgabe: {pandas_output}\n\n"
    "Antwort auf Deutsch: "
)

# Erstellen der Prompt-Templates und Parsers
pandas_prompt = PromptTemplate(pandas_prompt_str).partial_format(
    instruction_str=instruction_str, df_str=df.head(5).to_string()  # Convert DataFrame to string
)
pandas_output_parser = PandasInstructionParser(df)
response_synthesis_prompt = PromptTemplate(response_synthesis_prompt_str)
llm = OpenAI(api_key=api_key, model="gpt-4o")  

# Erstellen der QueryPipeline mit den Modulen
qp = QP(
    modules={
        "input": InputComponent(),
        "pandas_prompt": pandas_prompt,
        "llm1": llm,
        "pandas_output_parser": pandas_output_parser,
        "response_synthesis_prompt": response_synthesis_prompt,
        "llm2": llm,
    },
    verbose=True
)
# Hinzufügen der Ketten zur Pipeline
qp.add_chain(["input", "pandas_prompt", "llm1", "pandas_output_parser"])
# Hinzufügen der Links zwischen den Modulen
qp.add_links(
    [
        Link("input", "response_synthesis_prompt", dest_key="query_str"),
        Link("llm1", "response_synthesis_prompt", dest_key="pandas_instructions"),
        Link("pandas_output_parser", "response_synthesis_prompt", dest_key="pandas_output"),
    ]
)
# Hinzufügen des letzten Links
qp.add_link("response_synthesis_prompt", "llm2")

def query_agent(prompt, history):
    response = qp.run(query_str=prompt)
    message_obj = response.message  
    response_text = message_obj.content
    cleaned_response = response_text.replace("assistant: ", "", 1)
    history.append({"role": "user", "content": prompt})
    history.append({"role": "assistant", "content": cleaned_response})
    print(cleaned_response)
    return cleaned_response, history
