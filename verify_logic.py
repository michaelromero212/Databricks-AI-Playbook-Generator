import sys
import os
import yaml
from dotenv import load_dotenv

load_dotenv()

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from app.extractors.sql_extractor import SQLExtractor
from app.extractors.notebook_parser import NotebookParser
from app.extractors.py_analyzer import PyAnalyzer
from app.generators.diagram_generator import DiagramGenerator
from app.generators.playbook_generator import PlaybookGenerator

def verify():
    print("Starting Verification...")
    
    # 1. Test SQL Extractor
    print("\nTesting SQL Extractor...")
    sql_extractor = SQLExtractor()
    sql_file = "data/samples/bronze_to_silver.sql"
    if os.path.exists(sql_file):
        sql_meta = sql_extractor.parse_file(sql_file)
        print(f"SQL Metadata: {sql_meta}")
    else:
        print(f"Error: {sql_file} not found")

    # 2. Test Notebook Parser (Python source)
    print("\nTesting Notebook Parser (Py)...")
    nb_parser = NotebookParser()
    nb_file = "data/samples/sample_notebook.py"
    if os.path.exists(nb_file):
        nb_meta = nb_parser.parse_notebook(nb_file)
        print(f"Notebook Metadata: {nb_meta}")
    else:
        print(f"Error: {nb_file} not found")

    # 3. Test Diagram Generator
    print("\nTesting Diagram Generator...")
    diagram_gen = DiagramGenerator()
    analysis_results = {
        "bronze_to_silver.sql": sql_meta if 'sql_meta' in locals() else {},
        "sample_notebook.py": nb_meta if 'nb_meta' in locals() else {}
    }
    mermaid = diagram_gen.generate_mermaid(analysis_results)
    print(f"Mermaid Code:\n{mermaid}")

    # 4. Test Playbook Generator (Mock)
    print("\nTesting Playbook Generator...")
    playbook_gen = PlaybookGenerator()
    project_info = {"client": "Test Client", "objective": "Test Objective"}
    playbook = playbook_gen.generate_playbook(project_info, analysis_results, mermaid)
    print(f"Playbook Preview:\n{playbook[:200]}...")

    print("\nVerification Complete.")

if __name__ == "__main__":
    verify()
