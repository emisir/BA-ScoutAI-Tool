from llama_index.core.query_pipeline import (
    QueryPipeline as QP,
    Link,
    InputComponent as InputComponent,
)
from llama_index.experimental.query_engine.pandas import PandasInstructionParser as PandasInstructionParser
from llama_index.llms.openai import OpenAI
from llama_index.core.prompts import PromptTemplate as PromptTemplate
from dotenv import load_dotenv
import pandas as pd
import os

# Laden der Umgebungsvariablen aus einer .env Datei
load_dotenv()

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

# Anweisungen zur Umwandlung der Anfrage in ausführbaren Pandas-Code
instruction_str = (
    "1. Convert the query to executable Python code using Pandas.\n"
    "2. The final line of code should be a Python expression that can be called with the eval() function.\n"
    "3. The code should represent a solution to the query.\n"
    "4. PRINT ONLY THE EXPRESSION\n"
    "5. Do not quote the expression.\n"
)

# Vorlage für den Pandas-Prompt
pandas_prompt_str = (
    "You are working with a pandas dataframe in Python.\n"
    "The name of the dataframe is df.\n"
    "This is the result of print(df.head()):\n"
    "{df_str}\n\n"
    "Follow these instructions:\n"
    "{instruction_str}\n"
    "Query: {query_str}\n\n"
    "Expression:"
)

# Vorlage für die Synthese der Antwort
response_synthesis_prompt_str = (
    "Given an input question, synthesize a response from the query results.\n"
    "Query: {query_str}\n\n"
    "Pandas Instructions (optional):\n{pandas_instructions}\n\n"
    "Pandas Output: {pandas_output}\n\n"
    "Response: "
)

# Erstellen der Prompt-Templates und Parsers
pandas_prompt = PromptTemplate(pandas_prompt_str).partial_format(
    instruction_str=instruction_str, df_str=df.head(5).to_string()  # Convert DataFrame to string
)
pandas_output_parser = PandasInstructionParser(df)
response_synthesis_prompt = PromptTemplate(response_synthesis_prompt_str)
llm = OpenAI(model="gpt-4o")

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